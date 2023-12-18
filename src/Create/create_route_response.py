from pydantic import BaseModel

class CreateResponse(BaseModel):
    letter: str
    trad: str
    dico_id: int