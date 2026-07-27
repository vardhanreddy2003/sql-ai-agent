from pydantic import BaseModel,Field
from typing import Literal
class Query_evaluation(BaseModel):
  query:str=Field(description="generate SQL query for  user input")