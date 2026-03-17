import streamlit as st
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

BASE_MODEL = "Qwen/Qwen2-7B-Instruct"
ADAPTER = "Nemo30/QWEN_SPEC_TEST"

@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        device_map="auto",
        torch_dtype=torch.float16
    )
    model = PeftModel.from_pretrained(base_model, ADAPTER)
    model = model.merge_and_unload()
    model.eval()
    return tokenizer, model

tokenizer, model = load_model()

st.title("Specification QA Model (LoRA Fine-Tuned)")

question = st.text_area("Ask a question from the specification:")

if st.button("Generate Answer"):
    if question:
        prompt = f"""You are a technical specification assistant.
Answer strictly based on the specification.

Question:
{question}

Answer:"""

        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=512,
                temperature=0.2,
                top_p=0.9,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )

        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        st.write(response)