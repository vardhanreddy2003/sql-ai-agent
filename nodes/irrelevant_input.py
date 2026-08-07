
from graph.State import SQLAgentState
from langgraph.types import Command
from langgraph.graph import END
from typing import Literal

def irrelevant_input(state:SQLAgentState)->Command[Literal[END,"error_router"]]:
    try:
    
        return Command(
               update={
                      "result":"your request is irrelevant to the database. Please try a different command."
               },
               goto=END
        )
    except Exception as e:
                print("error at irrelevant_input",e)
                return Command(
                    update={
                        "Error": str(e)
                    },
                    goto="error_router"
                )