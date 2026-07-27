from click import prompt
from flask import json
from langgraph.graph import StateGraph,START,END
from langchain_core.prompts import PromptTemplate
from models.Summary_model import Summary_generator
from models.validation_model import validation_model_creation
from models.query_generator_model import query_generator
from typing import Literal
from graph.State import SQLAgentState


from nodes.intent_check import intent_check
from nodes.intent_classification import intent_classification
from nodes.build_query import build_query
from nodes.check_query import check_query
from nodes.is_destructive_sql import is_destructive_sql
from nodes.irrelevant_input import irrelevant_input
from nodes.opinion_on_info import opinion_on_info
from nodes.sql_harm_status import sql_harm_status
from nodes.harmful_input import harmful_input
from nodes.execute_sql import execute_sql_query
from nodes.summary import summary
from nodes.general_chat import general_chat

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

    graph.add_edge(START,"intent_classification")
    graph.add_conditional_edges("intent_classification",intent_check)
    graph.add_conditional_edges("check_query",opinion_on_info)
    graph.add_edge("irrelevant_input",END)
    graph.add_conditional_edges("is_destructive_sql",sql_harm_status)
    graph.add_edge("build_query","query_execution")
    graph.add_edge("query_execution",END)
    graph.add_edge("harmful_input",END)
    graph.add_edge("general_chat",END)
    workflow=graph.compile()
    return workflow
    