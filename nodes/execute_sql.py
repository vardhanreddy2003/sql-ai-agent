
from typing import Literal

from langgraph.types import Command

from graph.State import SQLAgentState
from db.DBConnection import getConnection
from langgraph.graph import END
import mysql.connector

def execute_sql_query(state:SQLAgentState)-> Command[Literal["error_router","remediate_sql","summary"]]:

    

    try:
        conn=getConnection()
        
        cursor=conn.cursor(dictionary=True)
        
        cursor.execute(state["query"])
        rows=cursor.fetchall()
        
        
        state["query_result"]=rows
        return Command(
            update={"query_result":rows},
            goto="summary"
        )
    except mysql.connector.Error as e:
        print("database error:",e)
        return Command(
            update={"database_error":str(e)},
            goto="remediate_sql"
        )
    except:
         return Command(
                            update={"Error":"error at execute sql"},
                            goto="error_router"
                        )
