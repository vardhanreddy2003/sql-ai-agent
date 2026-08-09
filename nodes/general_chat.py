from typing import Literal

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.types import Command
from langgraph.graph import END

from graph.State import SQLAgentState
from langchain_ollama import ChatOllama


def general_chat(
    state: SQLAgentState
) -> Command[Literal["error_router", END]]:

    try:
        print("chat history",state["chat_history"])

        model = ChatOllama(
            model="qwen:4b",
            temperature=0
        )

        print("came here")
      
        from langchain_core.prompts import PromptTemplate

        prompt = PromptTemplate(
            template="""
        You are a helpful AI assistant.

        Previous conversation:
        {chat_history}

        Current user question:
        {input}

        Use the previous conversation when it is relevant to answer
        the current question.
        """,
            input_variables=["chat_history", "input"]
        )
        prompt=prompt.invoke({"chat_history":state["chat_history"],"input":state["input"]})
        data=model.invoke(prompt)
            

        return Command(
            update={
                "result": data.content,
                "messages": AIMessage(content=data.content)
            },
            goto=END
        )

    except Exception as e:

        print("error at general_chat", e)

        return Command(
            update={
                "Error": str(e)
            },
            goto="error_router"
        )