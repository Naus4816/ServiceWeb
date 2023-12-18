from pydantic import BaseModel, Field
from typing import List, Dict

class ReadParams(BaseModel):
    mot: str