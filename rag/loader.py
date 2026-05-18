from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def load_pdf(pdf_path):
    """
    Loads PDF and returns LangChain Document objects.
    """

    # Create PDF loader
    loader = PyPDFLoader(pdf_path)

    # Load all pages
    documents = loader.load()

    return documents


def chunk_documents(documents):
    """
    Splits loaded documents into smaller chunks.
    """

    # Create text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )

    # Split documents into chunks
    chunks = text_splitter.split_documents(documents)

    return chunks