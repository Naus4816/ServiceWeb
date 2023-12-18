from pydantic import BaseModel, Field
from typing import List, Dict

class DeleteParams(BaseModel):
    name:str
