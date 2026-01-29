import chromadb

client = chromadb.Client()
collection = client.get_or_create_collection(name="my_collection")  


collection.upsert(
    documents=["This is a document about JS", "This document is about machine learning", "Natural language processing is a fascinating field"],
    ids=["doc1", "doc2", "doc3"]
)

query_texts=["Tell me about machine learning", "What is JS"]

results = collection.query(
    query_texts=query_texts,
    n_results=2
)


# {
#     'ids': [['doc2', 'doc3'], ['doc1', 'doc3']], 
#     'distances': [[0.3, 0.4], [0.2, 0.5]], 
#     'documents': [['This document is about machine learning', 'Natural language processing is a fascinating field'], ['This is a document about JS', 'Natural language processing is a fascinating field']], 
#     'metadatas': [None, None]
# }


for query_idx, query in enumerate(query_texts):
    print(f"QUERY: {query_idx + 1}: {query}")

    for result_idx, result in enumerate(results['documents'][query_idx]):
        print(f"Document {result_idx+1}: {result}")
        print(f"Distance {result_idx+1}: {results['distances'][query_idx][result_idx]}")
        print(f"ID {result_idx+1}: {results['ids'][query_idx][result_idx]}")
        print("\n")


