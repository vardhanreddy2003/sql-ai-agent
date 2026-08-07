from typing import TypedDict,Literal

class SQLAgentState(TypedDict):
    intent:Literal['sql_query','not_sql_query']
    input:str
    schema:str
    input_safety_status:str
    user_type:str
    opinion:Literal['yes','no']
    query_result:str
    result:str
    query:str
    summary:str
    Error:str
    database_error:str
    retry_count:int
    workflow_error:str