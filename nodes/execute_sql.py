
from graph.State import SQLAgentState
from db.DBConnection import getConnection

def execute_sql_query(state:SQLAgentState)->SQLAgentState:
    
    conn=getConnection()
    
    cursor=conn.cursor(dictionary=True)
        
    cursor.execute(state["query"])
    rows=cursor.fetchall()


    state["query_result"]=rows
    print("query_result",state["query_result"])
    return state
