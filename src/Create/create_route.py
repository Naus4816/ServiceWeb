from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .create_database import SessionLocal, Base
from .create_route_params import CreateParams
from .create_route_response import CreateResponse
from .create_models import Dico, Dico_Ligne
from typing import List, Tuple, Dict

create_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@create_router.post('/dico/{dico_name}', response_model=List[CreateResponse])
def Create(dico_name: str, params: CreateParams, db: Session = Depends(get_db)):
    # Récupérer l'ID du dictionnaire en fonction de son nom
    db_dico = db.query(Dico).filter(Dico.name.ilike(dico_name)).first()

    # Si le dictionnaire n'existe pas, créer un nouveau dictionnaire
    if not db_dico:
        # Créer et ajouter le dictionnaire
        db_dico = Dico(name=dico_name.strip())
        db.add(db_dico)
        db.commit()
        db.refresh(db_dico)

    # Définir les lettres
    letters = [chr(ord('a') + i) for i in range(26)]

    # Ajoute les lettres et traductions à la table Dict_Ligne
    result = []
    for letter in letters:
        # Récupérer la traduction associée à la lettre depuis le dictionnaire params.trads
        trad = params.trads.get(letter, "")

        existing_entry = db.query(Dico_Ligne).filter(Dico_Ligne.trad_id == db_dico.id, Dico_Ligne.letter == letter).first()

        if existing_entry:
            # Vérifie que la traduction du dictionnaire n'existe pas déjà
            raise HTTPException(status_code=400, detail=f"Une entrée pour la trad {trad} existe déjà dans le dictionnaire.")

        db_dico_ligne = Dico_Ligne(letter=letter, trad=trad, trad_id=db_dico.id)
        db.add(db_dico_ligne)
        result.append({
            'letter': letter,
            'trad': trad,
            'dico_id': db_dico.id,
        })

    db.commit()
    db.refresh(db_dico)

    return result
