from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from rag.loader import load_pdf, chunk_documents


# Path to medical PDF
PDF_PATH = "data/diabetes_guideline.pdf"

# Step 1 — Load PDF
documents = load_pdf(PDF_PATH)

print(f"Loaded {len(documents)} pages")


# Step 2 — Chunk documents
chunks = chunk_documents(documents)

print(f"Created {len(chunks)} chunks")


# Step 3 — Load embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding model loaded")


# Step 4 — Create FAISS vector database
vectorstore = FAISS.from_documents(
    documents=chunks,
    embedding=embedding_model
)

print("FAISS vector database created")


# Step 5 — Save FAISS index locally
vectorstore.save_local("faiss_index")

print("FAISS index saved successfully")
