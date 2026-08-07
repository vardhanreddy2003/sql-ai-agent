
from typing import Literal

from graph.State import SQLAgentState
from models.llm import model_creation
from models.llm import model_creation
from models.query_validation import Query_evaluation
from langchain_core.prompts import PromptTemplate
from langgraph.types import Command

def build_query(state:SQLAgentState)-> Command[Literal["query_execution","error_router"]]:

    
    try:
        prompt1 = PromptTemplate(
            template="""
        You are an expert SQL database analyst.


        Database schema:
        {schema}

        User request:
        {user_input}

        Instructions:
        1. Generate a valid SQL query that answers the user's request.
        2. Use ONLY the tables and columns present in the provided schema.
        3. Do NOT invent tables or columns.
        4. Return a single SQL query.
        5. Do NOT include explanations, comments, markdown, or code fences.
        6. If the request cannot be answered from the schema, return an empty query and explain the reason in the schema-defined output format.

        """,
            input_variables=["schema", "user_input"],
            validate_template=True
        
        )
        prompt=prompt1.invoke({"schema":state["schema"],"user_input":state["input"]})
        model=model_creation().with_structured_output(Query_evaluation)
        data=model.invoke(prompt)
        query=data.query
        
        return Command(
            update={"query":query},
            goto="query_execution"
        )
    except Exception as e:
        print("error at build_query",e)
        return Command(
            update={"Error":str(e)},
            goto="error_router"
        )