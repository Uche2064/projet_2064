from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.data.db import get_db
from app.data.oauth2 import oauth
from app.schema import schema
from app.utils import helpers
from app.model.model import Maison

router = APIRouter(
   tags=["Maison"],
   prefix="/maison"
)

@router.get("/", status_code=200)
async def get_user_houses(db: Annotated[Session, Depends(get_db)], current_user: Annotated[int, Depends(oauth.get_current_user)]):
   
   if not current_user:
      raise helpers.handleError(
         message="Vous n'êtes pas authentifier",
         code=401
      )
   house_list = db.query(Maison).filter(Maison.utilisateur_id == current_user.id).all()
   
   return {"data" : house_list}

@router.post("/", status_code=201)
async def save_user_house(maison: schema.SchemaMaison, db: Annotated[Session, Depends(get_db)], current_user: Annotated[int, Depends(oauth.get_current_user)]):
   if not current_user:
      raise helpers.handleError(
         message="Vous n'êtes pas authentifier",
         code=401
      )
   new_house = Maison(**maison.model_dump())
   
   db.add(new_house)
   db.commit()
   db.refresh(new_house)
   return new_house

@router.get("/{id}", status_code=200)
async def get_user_house_by_id(id: int, db: Annotated[Session, Depends(get_db)], current_user: Annotated[int, Depends(oauth.get_current_user)]):
   
   if not current_user:
      raise helpers.handleError(
         message="Vous n'êtes pas authentifier",
         code=401
      )
   house = db.query(Maison).filter(Maison.id == id).first()
   if house is None:
      raise helpers.handleError(
         message="Maison non trouvé",
         code=404
      )
   return house

@router.delete("/{id}", status_code=204)
async def get_user_house_by_id(id: int, db: Annotated[Session, Depends(get_db)], current_user: Annotated[int, Depends(oauth.get_current_user)]):
   
   if not current_user:
      raise helpers.handleError(
         message="Vous n'êtes pas authentifier",
         code=401
      )
   house = db.query(Maison).filter(Maison.id == id).first()
   if house is None:
      raise helpers.handleError(
         message="Maison non trouvé",
         code=404
      )
   db.delete(house)
   db.commit
   

@router.put("/{id}", status_code=200)
async def update_user_house(
   id: int,
   maison_update: schema.SchemaMaisonUpdate,
   db: Annotated[Session, Depends(get_db)],
   current_user: Annotated[int, Depends(oauth.get_current_user)]
):
   # Vérification de l'authentification de l'utilisateur
   if not current_user:
      raise helpers.handleError(
   message="Vous n'êtes pas authentifié",
   code=401
   )

   # Recherche de la maison à mettre à jour
   house = db.query(Maison).filter(Maison.id == id).first()
   if house is None:
      raise helpers.handleError(
   message="Maison non trouvée",
   code=404
   )

   # Mise à jour des informations de la maison
   for key, value in maison_update.model_dump().items():
      setattr(house, key, value)

   # Enregistrement des modifications dans la base de données
   db.commit()
   db.refresh(house)

   return house