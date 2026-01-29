import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import os
from pypdf import PdfReader
from openai import OpenAI

load_dotenv()

openai_client = OpenAI()

chroma_client = chromadb.PersistentClient(path="./chroma_db")

collection = chroma_client.get_or_create_collection(
    name="my_collection_openai_manual",
)


def split_text(text, chunk_size=500, chunk_overlap=50):
    """Split text into chunks"""
    step = chunk_size - chunk_overlap
    return [text[i:i+chunk_size] for i in range(0, len(text), step)]


def get_embeddings(text):
    """Get embeddings for text"""
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

directory = "./pdfs"
all_docs = []
all_ids = []
all_embeddings = []

for filename in os.listdir(directory):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(directory, filename)
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        chunks = split_text(text)
        for i, chunk in enumerate(chunks):
            all_docs.append(chunk)
            all_ids.append(f"{filename}_{i}")
            all_embeddings.append(get_embeddings(chunk))

collection.upsert(
    documents=all_docs,
    ids=all_ids,
    embeddings=all_embeddings
)

query = "When was the civil war?"
query_embedding = get_embeddings(query)
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)

for i, doc in enumerate(results['documents'][0]):
    print(f"Document {i+1}: {doc}")
    print(f"Distance {i+1}: {results['distances'][0][i]}")
    print(f"ID {i+1}: {results['ids'][0][i]}")
    print("\n")


print("Documents added and persisted!")

import pandas as pd


data = collection.get(include=["documents", "embeddings"])


print(pd.DataFrame({
    "document": [doc[:20] for doc in data["documents"]],
    "embedding": [emb[:20] for emb in data["embeddings"]],
    "id": data["ids"]
}))
