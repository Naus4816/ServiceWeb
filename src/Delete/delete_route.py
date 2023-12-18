from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .delete_database import SessionLocal, Base
from .delete_route_params import DeleteParams
from .delete_route_response import DeleteResponse
from .delete_models import Dico, Dico_Ligne

delete_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@delete_router.delete('/dico', response_model=DeleteResponse)
def Delete(dico_name: str, db: Session = Depends(get_db)):

    # Récupérer le dictionnaire en fonction de son nom
    db_dico = db.query(Dico).filter(Dico.name.ilike(dico_name)).first()

    # Vérifier que le dictionnaire existe
    if not db_dico:
        raise HTTPException(status_code=404, detail="Dictionnaire non trouvé")

    # Créer une liste de lettre de A à Z
    letters = [chr(ord('A') + i) for i in range(26)]

    # Supprimer chaque ligne de lettre
    for letter in letters:
        db_dico_ligne = db.query(Dico_Ligne).filter(Dico_Ligne.trad_id == db_dico.id, Dico_Ligne.letter == letter).first()
        if db_dico_ligne:
        # Supprimer l'entrée si elle existe
            db.delete(db_dico_ligne)
    # Supprimer le dictionnaire
    db.delete(db_dico)
    db.commit()

    return {
        'message':  f"Le dictionnaire {db_dico.name} a été supprimé avec succès"
    }
    
