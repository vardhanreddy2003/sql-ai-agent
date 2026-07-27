from graph.State import SQLAgentState
from langchain_ollama import ChatOllama

def general_chat(State:SQLAgentState)->SQLAgentState:
    model = ChatOllama(
        model="qwen:4b",
        temperature=0
    )
    data=model.invoke(State["input"])
    State["result"]=data.content
    return State