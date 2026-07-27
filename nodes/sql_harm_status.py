
from graph.State import SQLAgentState
from typing import Literal

def sql_harm_status(state:SQLAgentState)->Literal["build_query","harmful_input"]:

    harm_status=state["input_safety_status"]

    if harm_status=="safe":
        return "build_query"
    else:
        return "harmful_input"