from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .Create.create_route import create_router
from .Read.read_route import read_router
from .Update.update_route import update_router
from .Delete.delete_route import delete_router
from .models import Trad, Dico, Dico_Ligne
from .database import Base, engine, SessionLocal
from typing import List, Tuple, Dict

Base.metadata.create_all(bind=engine)


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from sqlalchemy.orm import Session

app.include_router(create_router, prefix="/create_route", tags=["create_route"])
app.include_router(read_router, prefix="/read_route", tags=["read_route"])
app.include_router(update_router, prefix="/update_route", tags=["update_route"])
app.include_router(delete_router, prefix="/delete_route", tags=["delete_route"])

