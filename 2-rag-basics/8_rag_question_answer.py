import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import os
from pypdf import PdfReader
from openai import OpenAI

load_dotenv()

openai_client = OpenAI()

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    model_name="text-embedding-3-small"
)

chroma_client = chromadb.PersistentClient(path="./chroma_db")

collection = chroma_client.get_or_create_collection(
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


def ask_question(question):
    results = collection.query(
        query_texts=[question],
        n_results=2
    )
    context = results['documents'][0][1]
    print(context)
    print("\n\n")
    prompt = f"""Use the following context to answer the question.
    Context: {context}
    Question: {question}
    If the answer is not in the context, say "I don't know".
    Answer: """
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

print(ask_question("What is civil war?"))
