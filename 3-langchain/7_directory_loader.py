from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
import os

# Construct path to the pdfs directory relative to this script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Navigate up to root then into 2-rag-basics/pdfs
pdfs_dir = os.path.join(current_dir, "./", "pdfs")

print(f"Loading PDFs from: {pdfs_dir}")

# Initialize DirectoryLoader to find all .pdf files and use PyPDFLoader for parsing
loader = DirectoryLoader(
    path=pdfs_dir,
    glob="**/*.pdf",
    loader_cls=PyPDFLoader,
    show_progress=True
)

docs = loader.load()

print(f"\nSuccessfully loaded {len(docs)} pages from directory.")
if docs:
    print("\n--- Example Content (First Document) ---")
    print(f"Source: {docs[0].metadata['source']}")
    print(f"Content Preview: {docs[0].page_content[:200]}...")
else:
    print("No documents found.")
