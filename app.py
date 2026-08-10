from flask import Flask,request,jsonify
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from langchain_core.messages import HumanMessage
from graph.Chatbot_graph import validation_graph
from db.DBConnection import getConnection
from rag.vectorstore import get_retriever
from nodes.retrieve_schema import retrieve_schema

from dotenv import load_dotenv
load_dotenv()
app=Flask(__name__)

CORS(app)

get_retriever()
@app.route("/")
def index():
    return "Testing 123"

@app.route("/getAnswer",methods=["POST"])
def answer():
    print("request received")
    data=request.get_json()
    question=data.get("question")
    thread_id=data.get("thread_id")
    print("thread_id", thread_id)
    config = {
    "configurable": {
        "thread_id": thread_id
    }
    }

    workflow=validation_graph()
    chat_history=workflow.get_state(config).values.get("messages",[])
    res=workflow.invoke({"input":question,"user_type":"user","messages":[HumanMessage(content=question)],"chat_history":chat_history},config=config)
    
   

    
    return jsonify(
        {
            "query":res.get("query",""),
            "query_result":res.get("query_result",None),
            "result":res.get("result",None),
            "Error":res.get("Error",None),
            "workflow_error":res.get("workflow_error",None),
            "database_error":res.get("database_error",None)
        }
    )

@app.route("/getAllDetails")
def getCustomerDetails():
    
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers")
        data = cursor.fetchall()

        print("DATA FROM DB:", data)

        return data

    except Exception as e:
        print("DB ERROR:", str(e))
        return str(e)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)