from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWT, PyJWTError
import jwt.exceptions
from app.schema import schema
from app.utils import helpers
from app.core.settings import setting


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def creer_token_acces(info_utilisateur: dict):
   to_encode = info_utilisateur.copy()
   expire = datetime.now(timezone.utc) + timedelta(minutes=setting.duree_acces)

   to_encode.update({"exp": expire})
   token = jwt.encode(payload=to_encode, key=setting.secret_key, algorithm=setting.algorithm)
   return token

def verify_token(token: str, credentials_exception):
   try:
      payload = dict(jwt.decode(jwt=token, key=setting.secret_key, algorithms=[setting.algorithm]))
      id: int = payload.get("id")
      email: str = payload.get("username")
      if id is None:
         raise credentials_exception
      return schema.TokenData(id=id, username=email)
   except PyJWTError:
      raise credentials_exception
   

def get_current_user(token: str = Depends(oauth2_scheme)):
   credentials_exception = helpers.handleError(
      message="Information invalide",
      code=401
   )

   return  verify_token(token, credentials_exception)