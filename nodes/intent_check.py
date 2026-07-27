
from typing import Literal

from graph.State import SQLAgentState


def intent_check(state:SQLAgentState)->Literal["check_query","general_chat"]:
    
   
    intent=state["intent"].strip().lower()
    print("intent_check",intent)
    if(intent=="sql_query"):
        return "check_query"
    else:
        
        return "general_chat"
