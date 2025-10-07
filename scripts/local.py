from langchain.llms import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain import PromptTemplate, LLMChain

# -------- Model setup --------
MODEL_ID = "deepseek-ai/deepseek-coder-1.3b-instruct"  # or any local HF model

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    device_map="auto",
    torch_dtype="auto"
)

generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=300,
    temperature=0.2,
    do_sample=True,
)

llm = HuggingFacePipeline(pipeline=generator)

# -------- Prompt + Chain --------
template = """
You are an expert software engineer.

Write only valid, complete {language} code (no explanations) that satisfies this request:
"{task}"
"""
prompt = PromptTemplate(
    input_variables=["language", "task"],
    template=template,
)

code_chain = LLMChain(llm=llm, prompt=prompt)

# -------- Use the agent --------
result = code_chain.run(language="Python", task="write a quicksort function")
print(result)
