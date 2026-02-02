from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

# Construct path to the pdfs directory relative to this script
current_dir = os.path.dirname(os.path.abspath(__file__))
pdfs_dir = os.path.join(current_dir, "./", "pdfs")

print(f"Loading PDFs from: {pdfs_dir}")

# Load all PDFs
loader = DirectoryLoader(
    path=pdfs_dir,
    glob="**/*.pdf",
    loader_cls=PyPDFLoader,
    show_progress=True
)

docs = loader.load()

print(f"Loaded {len(docs)} documents/pages from directory.")

# Initialize the recursive splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    add_start_index=True
)

# Split the documents
split_docs = text_splitter.split_documents(docs)

print(f"\nCreated {len(split_docs)} chunks from all PDFs.")

print("\n--- All Chunks ---")
for i, doc in enumerate(split_docs):
    print(f"\nChunk {i+1}:")
    # Truncate content for display if it's very long, or show all if user prefers. 
    # Showing first 200 chars to keep output readable but demonstrating access.
    print(f"Content: {doc.page_content[:200]}...") 
    print(f"Metadata: {doc.metadata}")
