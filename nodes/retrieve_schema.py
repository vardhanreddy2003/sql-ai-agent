

from typing import Literal

from langgraph.types import Command

from graph.State import SQLAgentState
from rag.vectorstore import get_retriever

def retrieve_schema(state:SQLAgentState)->Command[Literal["error_router","check_query"]]:
    try:
        retriever=get_retriever()
        schema_info=retriever.invoke(state["input"])
        schema=""
        
        schema = "\n".join(doc.page_content for doc in schema_info)
        return Command(
                                    update={
                                        "schema": schema
                                    },
                                    goto="check_query"
                                )
    except Exception as e:
                        return Command(
                            update={
                                "Error": str(e)
                            },
                            goto="error_router"
                        )

    
