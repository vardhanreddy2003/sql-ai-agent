from pydantic import BaseModel,Field
from typing import Literal

class Safeguard(BaseModel):
    safe_status:Literal["harm","safe"]=Field(description="safety of the user input")