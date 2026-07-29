

from graph.State import SQLAgentState
from rag.vectorstore import get_retriever

def retrieve_schema(state:SQLAgentState)->SQLAgentState:

    retriever=get_retriever()
    schema_info=retriever.invoke(state["input"])
    schema=""
    
    for i in range(0,len(schema_info)):
        schema+=schema_info[i].page_content
    state["schema"]=schema
    return state

    
