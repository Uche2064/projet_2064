import uuid
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from app.data.db import Base

class Maison(Base):
   __tablename__ = 'maisons'
   id = Column(Integer, primary_key=True, autoincrement=True)
   adresse = Column(String(256), nullable=False)
   prix = Column(Float, nullable=False)
   description = Column(String(256), nullable=False)
   photo = Column(String(256))
   statut = Column(String(256)) # à vendre ou à louer
   titre_foncier = Column(Boolean, default=True)
   longitude = Column(String(256))
   latitude = Column(String(256))
   utilisateur_id = Column(Integer, ForeignKey('utilisateurs.id'))

   utilisateur = relationship('Utilisateur', back_populates='maisons')

class Utilisateur(Base):
   __tablename__ = 'utilisateurs'
   id = Column(Integer, primary_key=True)
   nom_complet = Column(String(256), nullable=False)
   cni = Column(String(128), unique=True, nullable=False)
   email = Column(String(150), unique=True, nullable=False)
   mot_de_passe = Column(String(256), nullable=False)
   numero = Column(String(20), nullable=False)
   adresse = Column(String(256), nullable=False)
   photo = Column(String(256))
   date_creation = Column(TIMESTAMP, server_default=text("now()"), nullable=True)
   date_modification = Column(TIMESTAMP, server_default=text("now()"), nullable=True)
   
   maisons = relationship('Maison', back_populates='utilisateur')
   
