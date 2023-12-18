from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
    
from .update_database import SessionLocal, Base
from .update_route_params import UpdateParams
from .update_route_response import UpdateResponse
from .update_models import Dico, Dico_Ligne
from typing import List, Tuple, Dict

update_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@update_router.patch('/dico/{dico_name}/update', response_model=List[UpdateResponse])
def Update(dico_name: str, params: UpdateParams, db: Session = Depends(get_db)):
    # Récupérer l'ID du dictionnaire en fonction de son nom
    db_dico = db.query(Dico).filter(Dico.name.ilike(dico_name)).first()

    # Vérifier que le dictionnaire existe
    if not db_dico:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dictionnaire non trouvé")

    # Récupérer toutes les traductions existantes pour le dictionnaire
    existing_translations = {line.letter: line.trad for line in db.query(Dico_Ligne).filter(Dico_Ligne.trad_id == db_dico.id).all()}

    # Vérifie que la liste de traductions correspond au nombre de lettres
    if len(params.trads) != 26:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La liste de traductions doit contenir exactement 26 éléments")

    # Créer une liste de lettre de A à Z
    letters = [chr(ord('a') + i) for i in range(26)]

    # Parcourir les lettres et mettre à jour ou ajouter les traductions
    result = []
    for letter in letters:
        db_dico_ligne = db.query(Dico_Ligne).filter(Dico_Ligne.trad_id == db_dico.id, Dico_Ligne.letter == letter).first()
        trad = params.trads.get(letter, "")
        existing_trad = existing_translations.get(letter, "")

        if trad == "":
            # Si la traduction entrée par l'utilisateur est vide, utiliser la traduction existante
            trad = existing_trad

        if db_dico_ligne:
            # Mettre à jour l'entrée existante si elle existe
            db_dico_ligne.trad = trad
        else:
            # Ajouter une nouvelle entrée si elle n'existe pas
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