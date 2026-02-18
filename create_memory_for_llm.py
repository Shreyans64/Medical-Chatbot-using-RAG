from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
except ModuleNotFoundError:
    try:
        from langchain.text_splitters import RecursiveCharacterTextSplitter
    except Exception as _e:
        try:
            from langchain_text_splitters import RecursiveCharacterTextSplitter
        except Exception:
            raise ModuleNotFoundError(
                "Could not import langchain text splitter. "
                "Make sure you run this script with the Python interpreter that has `langchain` installed. "
                "For example: `C:\\Users\\gbsan\\anaconda3\\python.exe create_memory_for_llm.py` "
                "or install the packages into your current interpreter: `python -m pip install langchain langchain-text-splitters`"
            ) from _e
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

## Uncomment the following files if you're not using pipenv as your virtual environment manager
#from dotenv import load_dotenv, find_dotenv
#load_dotenv(find_dotenv())


# Step 1: Load raw PDF(s)
DATA_PATH="data"
def load_pdf_files(data):
    loader = DirectoryLoader(data,
                             glob='*.pdf',
                             loader_cls=PyPDFLoader)
    
    documents=loader.load()
    return documents

documents=load_pdf_files(data=DATA_PATH)
#print("Length of PDF pages: ", len(documents))

# Step 2: Split text into chunks
def split_documents(documents, chunk_size=500, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    text_chunks = text_splitter.split_documents(documents)
    return text_chunks

text_chunks = split_documents(documents)
print(f"Number of text chunks: {len(text_chunks)}")

# Step 3: Create embeddings and build FAISS vectorstore
def create_vectorstore(text_chunks, db_path="vectorstore/db_faiss"):
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.from_documents(text_chunks, embedding_model)
    db.save_local(db_path)
    print(f"Vectorstore saved to {db_path}")
    return db

db = create_vectorstore(text_chunks)
print("Vectorstore created successfully!")
