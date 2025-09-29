# scripts/load_website.py
from langchain_core.documents import Document
import requests
from bs4 import BeautifulSoup

MAX_CHARS = 200_000  # cap page size to reduce noise in retrieval

def load_website(url: str):
    html = requests.get(url, timeout=20).text[:MAX_CHARS]
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n")
    return [Document(page_content=text, metadata={"source": url, "doctype": "website"})]
