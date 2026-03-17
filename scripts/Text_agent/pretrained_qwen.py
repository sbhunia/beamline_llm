import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

BASE_MODEL = "Qwen/Qwen2-7B-Instruct"  # must match training base
ADAPTER = "Nemo30/QWEN_SPEC_TEST"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

print("Loading base model...")
base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    device_map="auto",
    torch_dtype=torch.float16
)

print("Loading LoRA adapter...")
model = PeftModel.from_pretrained(base_model, ADAPTER)

# Optional: merge for faster inference
print("Merging LoRA into base model...")
model = model.merge_and_unload()

model.eval()

def ask_model(question):
    prompt = f"""You are a technical specification assistant.
Answer strictly based on the specification knowledge.

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
    return response


if __name__ == "__main__":
    while True:
        q = input("\nAsk from spec: ")
        if q.lower() == "exit":
            break
        print("\n", ask_model(q))