    
from typing import Literal

from click import Command

from graph.State import SQLAgentState

from typing import Literal
from langgraph.graph import END
from langgraph.types import Command

def harmful_input(state: SQLAgentState) -> Command[Literal[END, "error_router","send_mail"]]:
    try:
        return Command(
            update={
                "result": "The user is not authorized to perform this operation. Please try a different command."
            },
            goto="send_mail"
        )

    except Exception as e:
        print("error at harmful_input", e)
        return Command(
            update={"Error": str(e)},
            goto="error_router"
        )