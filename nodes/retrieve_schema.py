

from graph.State import SQLAgentState
from rag.vectorstore import get_retriever

def retrieve_schema(state:SQLAgentState)->SQLAgentState:

    retriever=get_retriever()
    schema_info=retriever.invoke(state["input"])
    schema=""
    
    schema = "\n".join(doc.page_content for doc in schema_info)
    state["schema"]=schema
    return state

    
