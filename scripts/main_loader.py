from load_markdown import load_markdown_docs
# from load_images import load_images
from load_drive import load_drive_docs
from load_website import load_website
from load_spec_code import load_spec_macros


all_docs = []

all_docs += load_markdown_docs()
# all_docs += load_images()
all_docs += load_drive_docs()
all_docs += load_website("https://suchismitasarker.github.io/CHESS-ID4B-QM2/")
all_docs += load_spec_macros()


print(f"Total loaded document chunks: {len(all_docs)}")
