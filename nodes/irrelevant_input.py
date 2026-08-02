
from graph.State import SQLAgentState
from langgraph.types import Command
from langgraph.graph import END
from typing import Literal

def irrelevant_input(state:SQLAgentState)->Command[Literal[END,"error_router"]]:
    try:
    
        return Command(
               update={
                      "result":"can you please tell any sql requirement.I can help you with that"
               },
               goto=END
        )
    except Exception as e:
                return Command(
                    update={
                        "Error": str(e)
                    },
                    goto="error_router"
                )