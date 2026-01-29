import chromadb

from chromadb.utils import embedding_functions

default_ef = embedding_functions.DefaultEmbeddingFunction()

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="my_collection",
    embedding_function=default_ef
)

collection.add(
    documents=[
        "The quick brown fox jumps over the lazy dog.",
        "Artificial intelligence is transforming industries.",
        "ChromaDB is a vector database for AI applications."
    ],
    ids=["doc1", "doc2", "doc3"]
)

print("Documents added and persisted!")

results = collection.query(
    query_texts=["Who jumps over a lazy dog?"],
    n_results=3
)


# 5. Query the collection (even after restarting the script)

for i, doc in enumerate(results['documents'][0]):
    print(f"Document {i+1}: {doc}")
    print(f"Distance {i+1}: {results['distances'][0][i]}")
    print(f"ID {i+1}: {results['ids'][0][i]}")
    print("\n")


import pandas as pd


data = collection.get(include=["documents", "embeddings"])


print(pd.DataFrame({
    "document": [doc[:20] for doc in data["documents"]],
    "embedding": [emb[:20] for emb in data["embeddings"]]
}))