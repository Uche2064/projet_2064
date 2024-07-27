from fastapi import APIRouter, Depends, HTTPException, status
from app.data.oauth2 import oauth
from app.model.model import Utilisateur
from sqlalchemy.orm import Session
from app.data.db import get_db
from app.schema import schema
from app.utils import security, helpers
router = APIRouter(
   tags=["Utilisateur"],
   prefix="/utilisateur"
)


@router.post("/", status_code=201, response_model=schema.SchemaUtilisateurReponse)
async def save_user(user: schema.SchemaUtilisateur, db: Session = Depends(get_db)):
   # Vérification de l'unicité des champs
   helpers.check_unique_field(db, Utilisateur, Utilisateur.cni, user.cni, "cni")
   helpers.check_unique_field(db, Utilisateur, Utilisateur.numero, user.numero, "numéro")
   helpers.check_unique_field(db, Utilisateur, Utilisateur.email, user.email, "email")
   
   # Si aucune exception, on crée un nouvel utilisateur
   user.mot_de_passe = security.hash_password(user.mot_de_passe)
   new_user = Utilisateur(**user.model_dump(exclude_none=True))
   
   # on enregiste dans la base cet utilisateur
   db.add(new_user)
   db.commit()
   db.refresh(new_user)   
   # retourner une réponse
   return new_user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, current_user: int = Depends(oauth.get_current_user),  db: Session = Depends(get_db)):
   
   # checker si utilisateur existe
   get_db_user = db.query(Utilisateur).filter(Utilisateur.id == id).first()
   # sinon non, httpException
   if get_db_user is None:
      raise helpers.handleError(
         message=f"Utilisateur non trouvé",
         code=status.HTTP_404_NOT_FOUND,
      )
   # si oui supprimer utilisateur
   db.delete(get_db_user)
   db.commit()
   

# @router.put("/{id}", status_code=200, response_model=schema.SchemaUtilisateurReponse)
# async def update_user(
#    id: int,
#    user_update: schema.SchemaUtilisateur,
#    db: Session = Depends(get_db),
#    current_user: int = Depends(oauth.get_current_user)
# ):
#    # Vérifier si l'utilisateur existe
#    db_user = db.query(Utilisateur).filter(Utilisateur.id == id).first()
#    if db_user is None:
#       raise helpers.handleError(
#    message="Utilisateur non trouvé",
#    code=status.HTTP_404_NOT_FOUND,
#    )


#    # Mise à jour des champs
#    if user_update.cni and user_update.cni != db_user.cni:
#       helpers.check_unique_field(db, Utilisateur, Utilisateur.cni, user_update.cni, "cni")
#    if user_update.numero and user_update.numero != db_user.numero:
#       helpers.check_unique_field(db, Utilisateur, Utilisateur.numero, user_update.numero, "numéro")
#    if user_update.email and user_update.email != db_user.email:
#       helpers.check_unique_field(db, Utilisateur, Utilisateur.email, user_update.email, "email")

#    # Mise à jour des informations de l'utilisateur
#    for key, value in user_update.model_dump(exclude_none=True).items():
#       setattr(db_user, key, value)

#    # Hacher le mot de passe s'il est mis à jour
#    if user_update.mot_de_passe:
#       db_user.mot_de_passe = security.hash_password(user_update.mot_de_passe)

#    # Enregistrement des modifications dans la base de données
#    db.commit()
#    db.refresh(db_user)

#    return db_user
   
   
   