
from typing import Literal

from langgraph.types import Command

from graph.State import SQLAgentState
from db.DBConnection import getConnection
from langgraph.graph import END

def execute_sql_query(state:SQLAgentState)-> Command[Literal[END,"error_router"]]:

    

    try:
        conn=getConnection()
        
        cursor=conn.cursor(dictionary=True)
            
        cursor.execute(state["query"])
        rows=cursor.fetchall()


        state["query_result"]=rows
        return Command(
            update={"query_result":rows},
            goto=END
        )
    except:
         return Command(
                            update={"Error":"error at execute sql"},
                            goto="error_router"
                        )
