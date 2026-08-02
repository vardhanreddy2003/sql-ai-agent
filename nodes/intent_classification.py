from typing import Literal

from langgraph.types import Command
from langchain_core.prompts import PromptTemplate
from graph.State import SQLAgentState
from models.llm import model_creation
from models.Intent_classification import IntentClassification
def intent_classification(state:SQLAgentState)->Command[Literal["retrieve_schema","general_chat","error_router"]]:

    try:
        prompt=PromptTemplate(
                template = """
            
            You are an SQL intent classifier.

            Determine whether the user's request requires an SQL query to answer.

            Mark the intent as:
            - sql_query: if the request involves retrieving, inserting, updating, deleting, filtering, aggregating, or otherwise interacting with data in a database.
            - not_sql_query: for all other requests.

            Examples:

            Input: Show all customers.
            Intent: sql_query

            Input: Get details of all orders.
            Intent: sql_query

            Input: Delete customer 101.
            Intent: sql_query

            Input: Hello.
            Intent: not_sql_query

            Input: What is Python?
            Intent: not_sql_query

            User Request:
            {user_input}
            """,
                input_variables=["user_input"],
                
                validate_template=True
            )
        intent_prompt=prompt.invoke({"user_input":state.get("input")})
        model=model_creation().with_structured_output(IntentClassification)
        data=model.invoke(intent_prompt)
        
        state["intent"]=data.intent
        print("query",state["input"])
        intent=data.intent.strip().lower()
        print("intent_check",intent)
        if(intent=="sql_query"):
            return Command(
                 update={
                      "intent":intent
                 },
                 goto="retrieve_schema"
            )
        
        else:
             return Command(
                             update={
                                  "intent":intent
                             },
                             goto="general_chat"
                        )    
                 
    

    except Exception as e:
            return Command(
                update={
                    "Error": str(e)
                },
                goto="error_router"
            )
