from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from typing import List

import torch
from datasets import Dataset
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
    PeftModel,
)
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)

# ---------------------------------------------------------
# FIXED DATA PATHS
# ---------------------------------------------------------

PDF_DIR = "/home/vallurs/research/data/PDFs"
MD_DIR = "/home/vallurs/research/data/md_files"

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

@dataclass
class TrainConfig:
    base_model: str
    output_dir: str
    max_seq_length: int
    learning_rate: float
    num_train_epochs: float
    batch_size: int
    gradient_accumulation_steps: int
    logging_steps: int
    save_steps: int
    use_4bit: bool


# ---------------------------------------------------------
# DOCUMENT LOADING
# ---------------------------------------------------------

def load_pdf_docs(directory: str):
    docs = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".pdf"):
                path = os.path.join(root, file)
                loaded = PyPDFLoader(path).load()
                docs.extend(loaded)
    return docs


def load_md_docs(directory: str):
    docs = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".md"):
                path = os.path.join(root, file)
                loaded = TextLoader(path, encoding="utf-8").load()
                docs.extend(loaded)
    return docs


# ---------------------------------------------------------
# CHUNKING (SEPARATE STRATEGY)
# ---------------------------------------------------------

def chunk_documents(pdf_docs, md_docs):

    pdf_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    md_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
    )

    pdf_chunks = pdf_splitter.split_documents(pdf_docs)
    md_chunks = md_splitter.split_documents(md_docs)

    all_chunks = pdf_chunks + md_chunks

    texts = []
    for c in all_chunks:
        text = c.page_content.strip()
        if text:
            texts.append(text)

    return texts


# ---------------------------------------------------------
# TOKENIZATION
# ---------------------------------------------------------

def build_dataset(texts: List[str], tokenizer, max_seq_length: int):

    dataset = Dataset.from_dict({"text": texts})

    def tokenize(batch):
        tokens = tokenizer(
            batch["text"],
            truncation=True,
            max_length=max_seq_length,
            padding="max_length",
        )
        tokens["labels"] = tokens["input_ids"].copy()
        return tokens

    return dataset.map(tokenize, batched=True, remove_columns=["text"])


# ---------------------------------------------------------
# TRAINING
# ---------------------------------------------------------

def train(cfg: TrainConfig):

    print("Loading PDFs...")
    pdf_docs = load_pdf_docs(PDF_DIR)

    print("Loading Markdown files...")
    md_docs = load_md_docs(MD_DIR)

    if not pdf_docs and not md_docs:
        raise RuntimeError("No training documents found.")

    print("Chunking documents...")
    texts = chunk_documents(pdf_docs, md_docs)

    print(f"Total training chunks: {len(texts)}")

    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(cfg.base_model)
    tokenizer.pad_token = tokenizer.eos_token

    print("Building dataset...")
    dataset = build_dataset(texts, tokenizer, cfg.max_seq_length)

    print("Loading base model...")

    quant_config = None
    if cfg.use_4bit:
        quant_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
        )

    model = AutoModelForCausalLM.from_pretrained(
        cfg.base_model,
        quantization_config=quant_config,
        device_map="auto",
        torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
    )

    model.config.use_cache = False

    if cfg.use_4bit:
        model = prepare_model_for_kbit_training(
            model,
            use_gradient_checkpointing=True,
        )

    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        lora_dropout=0.1,
        bias="none",
        task_type="CAUSAL_LM",
    )

    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    training_args = TrainingArguments(
        output_dir=cfg.output_dir,
        per_device_train_batch_size=cfg.batch_size,
        gradient_accumulation_steps=cfg.gradient_accumulation_steps,
        num_train_epochs=cfg.num_train_epochs,
        learning_rate=cfg.learning_rate,
        bf16=torch.cuda.is_available(),
        logging_steps=cfg.logging_steps,
        save_steps=cfg.save_steps,
        optim="paged_adamw_8bit" if cfg.use_4bit else "adamw_torch",
        report_to="none",
        save_total_limit=2,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=DataCollatorForLanguageModeling(
            tokenizer=tokenizer,
            mlm=False,
        ),
    )

    print("Starting training...")
    trainer.train()

    print("Saving LoRA adapter...")
    model.save_pretrained(cfg.output_dir)

    print("Merging into full FP16 model...")

    base_model = AutoModelForCausalLM.from_pretrained(
        cfg.base_model,
        torch_dtype=torch.float16,
        device_map="auto",
    )

    merged_model = PeftModel.from_pretrained(base_model, cfg.output_dir)
    merged_model = merged_model.merge_and_unload()

    merged_dir = os.path.join(cfg.output_dir, "merged")
    merged_model.save_pretrained(
        merged_dir,
        safe_serialization=False
)
    tokenizer.save_pretrained(merged_dir)

    print(f"Final merged model saved to: {merged_dir}")


# ---------------------------------------------------------
# ARGPARSE
# ---------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--base-model", required=True)
    parser.add_argument("--output-dir", default="./finetuned-model")
    parser.add_argument("--max-seq-length", type=int, default=1024)
    parser.add_argument("--learning-rate", type=float, default=2e-4)
    parser.add_argument("--num-train-epochs", type=float, default=2.0)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--gradient-accumulation-steps", type=int, default=4)
    parser.add_argument("--logging-steps", type=int, default=10)
    parser.add_argument("--save-steps", type=int, default=100)
    parser.add_argument("--use-4bit", action="store_true")

    return TrainConfig(**vars(parser.parse_args()))


if __name__ == "__main__":
    config = parse_args()
    train(config)