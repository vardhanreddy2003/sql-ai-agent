from graph.State import SQLAgentState


def error_router(state:SQLAgentState):
    if state.get("error"):
        return "error_handler"
    return "success"