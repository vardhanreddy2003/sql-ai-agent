from pydantic import BaseModel,Field
from typing import Literal
class IntentClassification(BaseModel):
    intent:Literal["sql_query","not_sql_query"]=Field(description="opinion on the user input")