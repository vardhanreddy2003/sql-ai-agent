from typing import Literal

from langgraph.types import Command
from langgraph.graph import END

from graph.State import SQLAgentState
from langchain_ollama import ChatOllama

def general_chat(State:SQLAgentState)->Command[Literal["error_router",END]]:
    try:
        model = ChatOllama(
            model="qwen:4b",
            temperature=0
        )
        data=model.invoke(State["input"])
        State["result"]=data.content
        return Command(
            update={"result":data.content},
            goto=END
        )
    except Exception as e:
        print("error at general_chat",e)
        return Command(
                update={"Error":str(e)},
                   goto="error_router"
               ) 