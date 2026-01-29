import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import os
from pypdf import PdfReader
from openai import OpenAI
import json
import time

load_dotenv()

client = OpenAI()

reader = PdfReader("./pdfs/1 - Civil war - Wikipedia.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text()
chunks = [text[i:i+500] for i in range(0, len(text), 450)]

cache_file = "./cache.json"

times_without_cache = []

for run in range(1, 4):
    print(f"Run {run}")
    start_time = time.time()
    
    chroma_client = chromadb.Client()
    open_ef = embedding_functions.OpenAIEmbeddingFunction(
        model_name="text-embedding-3-small"
    )
    collection = chroma_client.get_or_create_collection(
        name=f"auto_{run}",
        embedding_function=open_ef
    )
    collection.upsert(
        documents=chunks,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )
    elapsed_time = time.time() - start_time
    times_without_cache.append(elapsed_time)
    print(f"Time: {elapsed_time}")


times_with_cache = []

cached_embeddings = None
for run in range(1, 4):
    print(f"Run {run}")
    start_time = time.time()

    
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            cached_embeddings = json.load(f)["embeddings"]
    else:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunks
        )
        cached_embeddings = [item.embedding for item in response.data]
        with open(cache_file, "w") as f:
            json.dump({'embeddings' : cached_embeddings}, f)

    chroma_client = chromadb.Client()            
    collection = chroma_client.get_or_create_collection(name=f"manual_{run}")
    collection.upsert(
        documents=chunks,
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        embeddings=cached_embeddings
    )

    elapsed_time = time.time() - start_time
    times_with_cache.append(elapsed_time)
    print(f"Time: {elapsed_time}")


print(sum(times_without_cache))
print(sum(times_with_cache))

    
