
from graph.State import SQLAgentState


def irrelevant_input(state:SQLAgentState):
    state["result"]="can you please tell any sql requirement.I can help you with that"
    return state