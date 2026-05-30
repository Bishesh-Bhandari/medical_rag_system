"""
ingest.py
Run this once to load the PDF, split it into chunks,
and build the FAISS index on disk.

Usage:
    python ingest.py
"""

from rag.loader import load_and_split
from rag.retriever import build_faiss_index


PDF_PATH = "data/diabetes_guideline.pdf"


def main() -> None:
    print("=" * 50)
    print("MediBot — Ingestion Pipeline")
    print("=" * 50)

    # Step 1: Load and split PDF
    print("\n[Step 1] Loading and splitting PDF...")
    chunks = load_and_split(
        path=PDF_PATH,
        chunk_size=500,
        chunk_overlap=50,
    )

    # Step 2: Build and save FAISS index
    print("\n[Step 2] Building FAISS index...")
    build_faiss_index(chunks)

    print("\n[Done] Ingestion complete. You can now run the app.")
    print("=" * 50)


if __name__ == "__main__":
    main()