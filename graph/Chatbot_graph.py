from click import prompt
from flask import json
from langgraph.graph import StateGraph,START,END
from langchain_core.prompts import PromptTemplate
from typing import Literal
from graph.State import SQLAgentState



from nodes.error_router import error_router
from nodes.intent_classification import intent_classification
from nodes.build_query import build_query
from nodes.check_query import check_query
from nodes.is_destructive_sql import is_destructive_sql
from nodes.irrelevant_input import irrelevant_input
from nodes.remediate_sql import remediate_sql
from nodes.harmful_input import harmful_input
from nodes.execute_sql import execute_sql_query
from nodes.summary import summary
from nodes.general_chat import general_chat
from nodes.retrieve_schema import retrieve_schema
from nodes.send_mail import send_alert_email
from nodes.search_query_memory import search_query_memory

def validation_graph():
    graph=StateGraph(SQLAgentState)

    graph.add_node("intent_classification",intent_classification)
    graph.add_node("check_query",check_query)
    graph.add_node("is_destructive_sql",is_destructive_sql)
    graph.add_node("irrelevant_input",irrelevant_input)
    graph.add_node("build_query",build_query)
    graph.add_node("harmful_input",harmful_input)
    graph.add_node("summary",summary)
    graph.add_node("query_execution",execute_sql_query)
    graph.add_node("general_chat",general_chat)
    graph.add_node("retrieve_schema",retrieve_schema)
    graph.add_node("error_router",error_router)
    graph.add_node("remediate_sql",remediate_sql)
    graph.add_node("send_mail",send_alert_email)
    graph.add_node("search_query_memory",search_query_memory)

    graph.add_edge(START, "intent_classification")

    workflow = graph.compile()
    return workflow