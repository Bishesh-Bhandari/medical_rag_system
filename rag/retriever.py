from langchain_community.vectorstores import FAISS

#same embedding model used during ingestion if not then the similarity search break cause different embedding model have different dimensional 
from ingest import embedding_model

#constant
FAISS_INDEX_PATH = "faiss_index"

#now we need to load the vectorstore 
def load_vectorstore():

    """
    Loads the saved FAISS vector database from disk.
    """

    vectorstore = FAISS.load_local(

        folder_path=FAISS_INDEX_PATH,

        embeddings=embedding_model,

        allow_dangerous_deserialization=True
    )

    return vectorstore

def retrieve_documents(query):
    vectorstore =load_vectorstore()
    results =vectorstore.similarity_search(query)

    return results


def get_similar_chunk(user_input):
    docs =retrieve_documents(user_input)

    response = ""

    for doc in docs:
        response += doc.page_content + "\n\n"

    return response
    
