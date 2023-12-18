from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base

class Trad(Base):
    __tablename__="trads"

    id = Column(Integer, primary_key=True, index=True)
    trad = Column(String(255))
    word = Column(String(40))
    dictionnary = Column(String(40))   

class  Dico(Base):
    __tablename__="dico"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))

    lines = relationship("Dico_Ligne", back_populates="dico")

class Dico_Ligne(Base):
    __tablename__="dico_ligne"

    id = Column(Integer, primary_key=True, index=True)
    letter = Column(String(8))
    trad = Column(String(8))
    trad_id = Column(Integer, ForeignKey("dico.id"))

    dico = relationship("Dico", back_populates="lines")
     

