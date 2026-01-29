import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import os
from pypdf import PdfReader

load_dotenv()

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    model_name="text-embedding-3-small"
)

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="my_collection_openai_pdf",
    embedding_function=openai_ef
)


def split_text(text, chunk_size=500, chunk_overlap=50):
    """Split text into chunks"""
    step = chunk_size - chunk_overlap
    return [text[i:i+chunk_size] for i in range(0, len(text), step)]

directory = "./pdfs"
all_docs = []
all_ids = []

for filename in os.listdir(directory):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(directory, filename)
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        chunks = split_text(text)
        all_docs.extend(chunks)
        all_ids.extend([f"{filename}_{i}" for i in range(len(chunks))])

collection.upsert(
    documents=all_docs,
    ids=all_ids
)

query_texts=["When was the civil war?", "What is civil war?"]
results = collection.query(
    query_texts=query_texts,
    n_results=2
)

for query_idx, query in enumerate(query_texts):
    print(f"QUERY: {query_idx + 1}: {query}")

    for result_idx, result in enumerate(results['documents'][query_idx]):
        print(f"Document {result_idx+1}: {result}")
        print(f"Distance {result_idx+1}: {results['distances'][query_idx][result_idx]}")
        print(f"ID {result_idx+1}: {results['ids'][query_idx][result_idx]}")
        print("\n")


print("Documents added and persisted!")

import pandas as pd


data = collection.get(include=["documents", "embeddings"])


print(pd.DataFrame({
    "document": [doc[:20] for doc in data["documents"]],
    "embedding": [emb[:20] for emb in data["embeddings"]],
    "id": data["ids"]
    
}))
