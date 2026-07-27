from pydantic import BaseModel,Field
from typing import Literal
class evaluation(BaseModel):
  opinion:Literal["yes","no"]=Field(description="opinion on the user input")