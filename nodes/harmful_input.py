    
from graph.State import SQLAgentState


def harmful_input(state:SQLAgentState):

    state["result"]="the user is not authorized to perform these operation. please try with a diff command"
    return state
