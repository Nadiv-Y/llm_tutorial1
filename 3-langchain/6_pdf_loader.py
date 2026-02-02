from langchain_community.document_loaders import PyPDFLoader
import os

# Construct path to the PDF file relative to this script
current_dir = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(current_dir, "./", "pdfs", "1 - Civil war - Wikipedia.pdf")

print(f"Loading PDF from: {pdf_path}")

loader = PyPDFLoader(pdf_path)
docs = loader.load()

print(f"Successfully loaded {len(docs)} pages.")
print("\n--- Page 1 Content View ---\n")
print(docs[0].page_content[:500])
print("...")
