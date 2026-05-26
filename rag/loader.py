from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_pdf(path):
    loader = PyPDFLoader(path)
    documents = loader.load()
    print(f"[loader] Loaded {len(documents)}")
    return documents 

def chunk(documents, chunk_size = 500, chunk_overlap = 50):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap)

    chunks = text_splitter.split_documents(documents)
    print(f"[loader] Created {len(chunks)} chunks")
    return chunks

def load_and_split(path, 
                    chunk_size = 500,
                    chunk_overlap = 50):
    
    documents = load_pdf(path)
    chunks = chunk(documents, chunk_size, chunk_overlap)
    return chunks