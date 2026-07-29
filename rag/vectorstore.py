from unittest import result

from models.embedding_model import embedding_model
from langchain_chroma import Chroma
from rag.schema_loader import load_schema_docs
from langchain_chroma import Chroma


docs = load_schema_docs()

def get_retriever():
    vectorstore = Chroma(
        collection_name="schemas",
        persist_directory="schema_db",
        embedding_function=embedding_model()
    )

    if vectorstore._collection.count() == 0:
        vectorstore.add_documents(docs)
        print("Documents added to Chroma.")
    else:
        print("Existing vector store loaded.")
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    

    return retriever