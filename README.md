MEDICAL-CHATBOT-USING-RAG
===============

Small local knowledge-base + chat UI that builds a FAISS vectorstore from PDFs and uses a local LLM endpoint (HuggingFace Endpoint) to answer queries.

Quick Overview
--------------
- `create_memory_for_llm.py`: Load PDFs from `data/`, split text, create embeddings and save a FAISS vectorstore under `vectorstore/db_faiss/`.
- `.vscode/create_memory_llm.py`: Example script that loads the vectorstore and runs a RetrievalQA pipeline (for quick CLI testing).
- `medibot.py`: Streamlit chat UI that queries the vectorstore and a Hugging Face LLM endpoint.

Prerequisites
-------------
- Use the same Python interpreter for installing dependencies and running the app (the repository was developed with an Anaconda Python installation).
- A Hugging Face endpoint token if you plan to use `HuggingFaceEndpoint`. Set it in the environment variable `HF_TOKEN`.

Recommended interpreter (example from this workspace):
- `C:\Users\gbsan\anaconda3\python.exe`

Install dependencies
--------------------
Using the interpreter you will run the app with (replace with your python path if different):

PowerShell (recommended):

```powershell
C:\Users\gbsan\anaconda3\python.exe -m pip install -r requirements.txt
```

Or install manually:

```powershell
C:\Users\gbsan\anaconda3\python.exe -m pip install streamlit langchain langchain-text-splitters langchain-huggingface langchain-community langchain-classic sentence-transformers torch transformers safetensors faiss-cpu reportlab
```

Notes:
- `faiss-cpu` binary availability depends on your Python version and platform. If `faiss-cpu` fails to install via pip on Windows, you may already have a working faiss wheel in your environment (this project used the system's installed FAISS).
- If you don't need local model embeddings, you can change the embedding backend.

Create the vectorstore (one-time, after adding PDFs)
---------------------------------------------------
1. Put your PDF files into the `data/` folder (create it if missing).
2. Run the script that builds the vectorstore:

```powershell
C:\Users\gbsan\anaconda3\python.exe create_memory_for_llm.py
```

This will:
- Load PDFs from `data/`
- Split documents into chunks
- Create embeddings using `sentence-transformers/all-MiniLM-L6-v2`
- Save FAISS index to `vectorstore/db_faiss/`

Run the Streamlit UI (medibot)
------------------------------
Start the Streamlit app using the Streamlit runner (this enables session state and correct runtime behavior):

```powershell
C:\Users\gbsan\anaconda3\python.exe -m streamlit run medibot.py
```

If you prefer a specific port:

```powershell
C:\Users\gbsan\anaconda3\python.exe -m streamlit run medibot.py --server.port 8502
```

Environment variables
---------------------
Set your Hugging Face token (example for current PowerShell session):

```powershell
$env:HF_TOKEN = "your_hf_token_here"
```

Troubleshooting
---------------
- Warning: "missing ScriptRunContext" or "Session state does not function when running a script without `streamlit run`" occurs if you run the script with plain `python medibot.py`. Always use the Streamlit runner.
- If you see errors from `torch` or the Streamlit watcher (e.g., introspection/runtime errors), the code now performs lazy imports of heavy libraries to avoid Streamlit's module watcher issues. Make sure you run the app with the same interpreter where the packages are installed.
- If FAISS fails to load when calling `FAISS.load_local(...)`, ensure `vectorstore/db_faiss/index.faiss` exists. Re-run `create_memory_for_llm.py` after adding PDFs to `data/`.

Adding or updating content
-------------------------
- To add documents, place PDFs in `data/` and re-run `create_memory_for_llm.py` to recreate the vectorstore.
- You can tweak chunk size / overlap inside `create_memory_for_llm.py`'s `split_documents` function.

Files of interest
-----------------
- `create_memory_for_llm.py` — build the vectorstore
- `medibot.py` — Streamlit chat app
- `vectorstore/` — contains saved FAISS vectorstore after running the builder
