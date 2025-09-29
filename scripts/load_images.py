from langchain_core.documents import Document
from PIL import Image
import pytesseract
import os

def load_images():
    docs = []
    img_dir = "data/image_docs"
    for fname in os.listdir(img_dir):
        if fname.lower().endswith((".png", ".jpg", ".jpeg")):
            path = os.path.join(img_dir, fname)
            text = pytesseract.image_to_string(Image.open(path))
            docs.append(Document(page_content=text, metadata={"source": fname}))
    return docs
