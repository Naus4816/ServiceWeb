from pydantic import BaseModel

class UpdateResponse(BaseModel):
    letter: str
    trad: str
    dico_id: int