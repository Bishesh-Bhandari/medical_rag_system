from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from .loader import chunk, load_pdf
from pathlib import Path

FAISS_INDEX_PATH = "faiss_index"


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name = 'sentence-transformers/all-MiniLM-L6-v2'
    )


project_root = Path(__file__).resolve().parents[1]
pdf_path = project_root / "data" / "diabetes_guideline.pdf"
document = load_pdf(str(pdf_path))
chunks = chunk(document)


def build_faiss_index(chunks):
    print("[retriever] Building FAISS index...")
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(
        chunks,
        embedding = embeddings
    )
    vectorstore.save_local(FAISS_INDEX_PATH)
    print("[retriever] FAISS index built and saved successfully")
    return vectorstore


def load_faiss_index():

    """
    Loads the saved FAISS vector database from disk.
    """
    index_path = Path(FAISS_INDEX_PATH)
    if not index_path.exists():
        return FileNotFoundError(f"FAISS index not found at {FAISS_INDEX_PATH}." 
                                 "Please run ingest.py first.")
    
    embeddings = get_embeddings()
    vectorstore = FAISS.load_local(

        folder_path=FAISS_INDEX_PATH,

        embeddings=embeddings,

        allow_dangerous_deserialization=True
    )

    return vectorstore


def get_retreiver(k : int =3 ):
    vectorestore = load_faiss_index()
    retrieved = vectorestore.as_retriever(
        search_type = "similarity",
        search_kwargs = {"k": k}
    )
    return retrieved
