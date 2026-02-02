# How to Run the Streamlit RAG App

To run the app correctly, you need to use the Python interpreter from the virtual environment where your dependencies (like `chromadb`) are installed.

## Command

Run the following command from the `llm-tutorial` directory:

```powershell
.\venv\Scripts\python -m streamlit run 2-rag-basics/9_rag_streamlit_app.py
```

## Why this command?

- `.\venv\Scripts\python`: Uses the Python executable inside your `venv` folder. This environment has `chromadb` and other libraries installed.
- `-m streamlit`: Runs the Streamlit module installed in that environment.
