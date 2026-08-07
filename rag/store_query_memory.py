

from rag.query_vectorstore import query_vectorstore
import hashlib

def store_query_memory(user_request:str,query:str,schema:str):
    try:
        queryVectorStore=query_vectorstore()
        

        

        user_request_id = hashlib.sha256(user_request.strip().lower().encode()).hexdigest()

        queryVectorStore.add_texts(
            texts=[user_request],
            ids=[user_request_id],
            metadatas=[{"query": query, "schema": schema}]
        )
        print(queryVectorStore._collection.count())
    except Exception as e:
        print("Error storing query memory:", str(e))
        