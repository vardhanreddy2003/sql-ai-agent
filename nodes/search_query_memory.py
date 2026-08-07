
from typing import Literal
from langgraph.types import Command
from graph.State import SQLAgentState
from rag.query_vectorstore import query_vectorstore

def search_query_memory(state:SQLAgentState)->Command[Literal["error_router","retrieve_schema","query_execution"]]:
    try:
        user_request=state.get("input")
        result=query_vectorstore().similarity_search_with_score(user_request, k=1)
        if result is None or len(result)==0:
            return Command(
                            goto="retrieve_schema"
            )
        doc,score=result[0]
        if result is None or len(result)==0:
            return Command(
                            goto="retrieve_schema"
                        )

        print("came here in search_query_memory")
        print("score",score)
        if(score<0.15):
            print("score is less than 0.15, going to query_execution")
            return Command(
                update={
                        "query":doc.metadata.get("query"),
                        "schema":doc.metadata.get("schema")
                    },
                goto="query_execution"
            )
            
        
        return Command(
                goto="retrieve_schema"
            )
        
    except Exception as e:
        print("Error searching query memory:", str(e))
        return Command(
            update={'Error':str(e)},
            goto="error_router"
        )