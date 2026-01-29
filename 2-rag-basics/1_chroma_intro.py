import chromadb

client = chromadb.Client()
collection = client.get_or_create_collection(name="my_collection")

collection.upsert(
    documents=["This is a document about JS", "Dolphins are cool", "Dogs are cool"],
    ids=["doc1", "doc2", "doc3"]
)

results = collection.query(
    query_texts=["Tell me about machine learning"],
    n_results=2
)


# {
#     'ids': [['doc2', 'doc3']], 
#     'distances': [[0.3, 0.4]], 
#     'documents': [['This document is about machine learning', 'Natural language processing is a fascinating field']], 
#     'metadatas': [None, None]
# }


for i, doc in enumerate(results['documents'][0]):
    print(f"Document {i+1}: {doc}")
    print(f"Distance {i+1}: {results['distances'][0][i]}")
    print(f"ID {i+1}: {results['ids'][0][i]}")
    print("\n")