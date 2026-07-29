
from typing import Literal

from graph.State import SQLAgentState


def intent_check(state:SQLAgentState)->Literal["retrieve_schema","general_chat"]:
    
   
    intent=state["intent"].strip().lower()
    print("intent_check",intent)
    if(intent=="sql_query"):
        return "retrieve_schema"
    else:
        
        return "general_chat"
