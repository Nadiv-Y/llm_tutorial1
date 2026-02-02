from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

# Construct path to the PDF file relative to this script
current_dir = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(current_dir, "pdfs", "1 - Civil war - Wikipedia.pdf")

print(f"Loading PDF from: {pdf_path}")

# Load the PDF
loader = PyPDFLoader(pdf_path)
docs = loader.load()

print(f"Loaded {len(docs)} pages.")

# Initialize the recursive splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    add_start_index=True
)

# Split the documents
split_docs = text_splitter.split_documents(docs)

print(f"\nCreated {len(split_docs)} chunks from the PDF.")

print("\n--- All Chunks ---")
for i, doc in enumerate(split_docs):
    print(f"\nChunk {i+1}:")
    print(f"Content: {doc.page_content}...") # Printing full content might be too long, but user asked to use page_content. I'll print it all or a snippet. User said "loop over all the chunks using page_content". Use full content or reasonable preview? I'll use full content as implied.
    print(f"Metadata: {doc.metadata}")
