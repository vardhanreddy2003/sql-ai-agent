
from graph.State import SQLAgentState
from models.llm import model_creation
from langchain_core.prompts import PromptTemplate

def summary(state:SQLAgentState):
    summaryModel=model_creation()
    summary_prompt = PromptTemplate(
    input_variables=["user_request", "sql_data"],
        template="""
    You are a helpful data analyst assistant. Your task is to create a clear and concise summary of SQL query results.

    **User Request:**
    {user_request}

    **SQL Query Results:**
    {sql_data}

    **Instructions:**
    - Provide a natural language summary of the data
    - Highlight key insights and patterns
    - Use clear, non-technical language
    - If the data is empty, explain that no results were found
    - Format numbers appropriately (use commas, percentages, etc.)

    **Summary:**
    """
    )
    prompt=summary_prompt.invoke({"user_request":state["input"],"sql_data":state["result"]})
    res=summaryModel.invoke(prompt)
    state["summary"]=res.content
    return state