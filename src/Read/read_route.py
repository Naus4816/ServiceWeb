from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .read_database import SessionLocal, Base
from .read_route_params import ReadParams
from .read_route_response import ReadResponse
from .read_models import Dico, Dico_Ligne
from typing import List, Tuple, Dict

read_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@read_router.post('/dico/{dico_name}/trad', response_model=ReadResponse)
def Read(params: ReadParams, dico_name: str, db: Session = Depends(get_db)):
    # Récupérer l'ID du dictionnaire en fonction de son nom
    db_dico = db.query(Dico).filter(Dico.name.ilike(dico_name)).first()

    # Vérifier que le dictionnaire existe
    if not db_dico:
        raise HTTPException(status_code=404, detail="Dictionnaire non trouvé")
    letters = list(params.mot)

    result = ""
    for i,letter in enumerate(letters):
        db_dico_ligne = db.query(Dico_Ligne).filter(Dico_Ligne.trad_id == db_dico.id, Dico_Ligne.letter == letter).first()
        result += db_dico_ligne.trad
        if i < len(letters) - 1: #Ajout d'un espace avant chaque lettre pour plus de lisibilité
            result += " "

    return ReadResponse(trad=result)