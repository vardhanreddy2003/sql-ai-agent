from typing import Literal

from langchain_core.prompts import PromptTemplate
from graph.State import SQLAgentState
from models.Safeguard import Safeguard
from models.llm import model_creation
from langgraph.types import Command

def is_destructive_sql(state:SQLAgentState)->Command[Literal["build_query","harmful_input","error_router"]]:
    try:
        input=state["input"]
        prompt=PromptTemplate(
            template='''
            You are a database safety classifier.

        

            Your only task is to determine whether a user's request {user_request} is safe to execute on a read-only SQL database.

            Allow only operations that retrieve data.

            Block any request that attempts to:

            - INSERT
            - UPDATE
            - DELETE
            - DROP
            - ALTER
            - CREATE
            - TRUNCATE
            - REPLACE
            - MERGE
            - GRANT
            - REVOKE
            - EXECUTE stored procedures
            - Any request that modifies data
            - Any request asking to remove, edit, rename, overwrite, or change records.

            Also block requests that indirectly ask to modify data, even if SQL keywords are not explicitly mentioned.

            Return exactly one value:
            - "harm" if the user request is harmful to the SQL database.
            - "safe" if the user request is not harmful to the SQL database.
            
            ''',
            input_variables=["user_request"],
            
            validate_template=True
        )
        prompt=prompt.invoke({"user_request":input})

        model=model_creation().with_structured_output(Safeguard)
        data=model.invoke(prompt)
        
    
        if data.safe_status=="safe":
    
            return Command(
                   update={
                          "input_safety_status":"safe"
                   },
                   goto="build_query"
            )
        else:
            return Command(
                    update={
                    "input_safety_status":"harm"
                    },
                    goto="harmful_input"
                )
    except Exception as e:
                    return Command(
                        update={
                            "Error": str(e)
                        },
                        goto="error_router"
                    )