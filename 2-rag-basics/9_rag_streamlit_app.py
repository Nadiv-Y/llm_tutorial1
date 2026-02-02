import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import os
from pypdf import PdfReader
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# Initialize Embedding Function
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    model_name="text-embedding-3-small"
)

@st.cache_resource
def get_chroma_collection():
    """
    Initialize ChromaDB client and collection.
    Cached to avoid reloading on every interaction.
    """
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    chroma_db_path = os.path.join(current_dir, "chroma_db")
    
    chroma_client = chromadb.PersistentClient(path=chroma_db_path)
    collection = chroma_client.get_or_create_collection(
        name="my_collection_openai_pdf",
        embedding_function=openai_ef
    )
    return collection

def split_text(text, chunk_size=500, chunk_overlap=50):
    """Split text into chunks"""
    step = chunk_size - chunk_overlap
    return [text[i:i+chunk_size] for i in range(0, len(text), step)]

def process_pdfs(directory, collection):
    """
    Process PDFs from the directory and add them to the collection.
    """
    # Resolve directory path relative to script if it's a relative path starting with ./ or .
    if directory.startswith("./") or directory.startswith(".\\"):
         current_dir = os.path.dirname(os.path.abspath(__file__))
         # Remove the ./ or .\ part
         stripped_dir = directory[2:] 
         directory = os.path.join(current_dir, stripped_dir)

    all_docs = []
    all_ids = []
    
    if not os.path.exists(directory):
        st.error(f"Directory {directory} does not exist.")
        return 0

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
    
    if all_docs:
        collection.upsert(
            documents=all_docs,
            ids=all_ids
        )
    
    return len(all_ids)

def query_collection(collection, question):
    """
    Query the collection and get the answer from OpenAI.
    """
    results = collection.query(
        query_texts=[question],
        n_results=2
    )
    
    if not results['documents'][0]:
        return "No relevant context found.", ""

    context = results['documents'][0][0] # Taking the top result
    # Alternatively merge top results: "\n".join(results['documents'][0])
    
    prompt = f"""Use the following context to answer the question.
    Context: {context}
    Question: {question}
    If the answer is not in the context, say "I don't know".
    Answer: """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content, context

# --- Streamlit UI ---

st.title("📄 PDF RAG Question Answering")

# Initialize collection
collection = get_chroma_collection()

# Initialize session state for answer
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for processing PDFs
with st.sidebar:
    st.header("Configuration")
    if st.button("Process PDFs in ./pdfs"):
        with st.spinner("Processing PDFs..."):
            count = process_pdfs("./pdfs", collection)
            st.success(f"Processed and added {count} chunks to the database.")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Main Interface
if question := st.chat_input("Ask a question about your documents:"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": question})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer, context = query_collection(collection, question)
            st.markdown(answer)
            with st.expander("View Retrieved Context"):
                st.info(context)
            
    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": answer})
