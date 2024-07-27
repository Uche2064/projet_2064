from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.data.oauth2 import oauth
from app.model.model import Utilisateur
from sqlalchemy.orm import Session
from app.data.db import get_db
from app.utils import helpers, security

router = APIRouter(
   tags=["Authentification"],
   prefix="/login"
)

@router.get("/")
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
   db_user = db.query(Utilisateur).filter(Utilisateur.email == form_data.username).first()
   # checker si l'utilisateur existe
   if db_user is None:
      raise helpers.handleError(
         message="Information invalide",
         code=403
      )
   # si oui, checker son mot de passe
   if not security.verify_password(secret=form_data.password, hash=db_user.mot_de_passe):
      raise helpers.handleError(
         message="Information invalide",
         code=403
      )
   # creer le token d'acces si tout se passe bien
   token =  oauth.creer_token_acces({"username": db_user.email, "id": db_user.id})
   return {"access_token": token, "bearer": "token_bearer"}
   