from graph.State import SQLAgentState


def error_router(state:SQLAgentState)-> SQLAgentState:
    state["workflow_error"]="An error occured during the workflow execution,please try after some time"
    return state