from fastapi import HTTPException
from sqlalchemy.orm import Session


# Fonction pour vérifier l'unicité des champs
def check_unique_field(db: Session, model, field, value, field_name: str):
   if db.query(model).filter(field == value).first():
      raise handleError(message=f"{field_name} existe déjà", code=400)
   
   
def handleError(message: str, code: int):
   return HTTPException(
      status_code=code, 
      detail=message
   )