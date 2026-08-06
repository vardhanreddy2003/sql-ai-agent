from langchain_community.vectorstores import Chroma

from models.embedding_model import embedding_model

def query_vectorstore():
    vectorstore = Chroma(
        collection_name="queries",
        persist_directory="query_db",
        embedding_function=embedding_model()
    )
    return vectorstore