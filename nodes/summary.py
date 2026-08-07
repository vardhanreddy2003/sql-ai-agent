
from graph.State import SQLAgentState
from models.llm import model_creation
from langchain_core.prompts import PromptTemplate
from langgraph.graph import END
from langgraph.types import Command
from rag import store_query_memory
from rag.store_query_memory import store_query_memory
from typing import Literal
def summary(state:SQLAgentState)-> Command[Literal["error_router",END]]:
    summaryModel=model_creation()

    store_query_memory(state["input"], state["query"], state["schema"])

    summary_prompt = PromptTemplate(
    input_variables=["query","table_schemas"],
        template="""
    You are a helpful assistant that can help document SQL queries.

    Please document below SQL query by the given table schemas.

    ===SQL Query
    {query}

    ===Table Schemas
    {table_schemas}

    ===Response Guidelines
    Please provide the following list of descriptions for the query:
    -The selected columns and their description
    -The input tables of the query and the join pattern
    -Query's detailed transformation logic in plain english, and why these 
    transformation are necessary
    -The type of filters performed by the query, and why these filters are necessary
    -Write very detailed purposes and motives of the query in detail
    -Write possible improvements or suggestions for purposes of the query





    You are a helpful assistant that can help document SQL queries.

    Please document below SQL query by the given table schemas.

    ===SQL Query
    {query}

    ===Table Schemas
    {table_schemas}

    ===Response Guidelines
    Please provide the following list of descriptions for the query:
    -The selected columns and their description
    -The input tables of the query and the join pattern
    -Query's detailed transformation logic in plain english, and why these 
    transformation are necessary
    -The type of filters performed by the query, and why these filters are necessary
    -Write very detailed purposes and motives of the query in detail
    -Write possible improvements or suggestions for purposes of the query

    """




    )
    try:
        prompt=summary_prompt.invoke({"query":state["query"],"table_schemas":state["schema"]})
        res=summaryModel.invoke(prompt)
        
        return Command(
            update={"summary":res.content},
            goto=END
        )
    except:
        return Command(
            update={"Error":"error at summary node"},
            goto="error_router"
        )