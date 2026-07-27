
from graph.State import SQLAgentState
from typing import Literal

def opinion_on_info(state:SQLAgentState)->Literal["build_query",'irrelevant_input',"is_destructive_sql"]:
    opinion=state.get("opinion","").strip().lower()
    
    if(opinion.startswith("yes")):
        if(state["user_type"]=="user"):
            return "is_destructive_sql"
        else:
            return "build_query"

    else:
        return "irrelevant_input"