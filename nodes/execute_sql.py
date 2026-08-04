
from typing import Literal

from langgraph.types import Command

from graph.State import SQLAgentState
from db.DBConnection import getConnection
from langgraph.graph import END
import mysql.connector

def execute_sql_query(state:SQLAgentState)-> Command[Literal[END,"error_router","remediate_sql"]]:

    

    try:
        conn=getConnection()
        
        cursor=conn.cursor(dictionary=True)
        print("exceutinh exceute node") 
        cursor.execute("se")
        rows=cursor.fetchall()
        
        
        state["query_result"]=rows
        return Command(
            update={"query_result":rows},
            goto=END
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
