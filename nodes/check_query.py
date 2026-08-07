
from typing import Literal
from zipfile import Path
from langgraph.types import Command
from langchain_core.prompts import PromptTemplate
from graph.State import SQLAgentState
from models.Evaluation import evaluation
from models.Evaluation import evaluation
from models.llm import model_creation


def check_query(state:SQLAgentState)-> Command[Literal["error_router","irrelevant_input","build_query"]]:
        
    try:
        prompt= PromptTemplate(
            template="""
        Assume you are a database analyst.

    

        Available tables:
        {schema}
        user_input:
        {user_input}
        
        Determine whether the user's request can be answered using only the available tables.

        Return exactly one value:
        - "yes" if the request can be answered from the tables
        - "no" if it cannot

        Do not return any explanation or additional text.
        """,
        input_variables=["schema","user_input"],
    
        validate_template=True,
        )
        prompt1=prompt.invoke({"schema":state["schema"],"user_input":state.get("input")});
        model=model_creation().with_structured_output(evaluation)
        data=model.invoke(prompt1)
        
        

        state["opinion"]=data.opinion
        if(data.opinion.startswith("yes")):
                return Command(
                      update={"opinion":"yes"},
                      goto="build_query"
                )
        else:
            return Command(
                 update={"opinion":"no"},
                 goto="irrelevant_input"
            )                
    except Exception as e:
        print("error at check_query",e)
        return Command(
                update={"Error":str(e)},
                    goto="error_router"
                )