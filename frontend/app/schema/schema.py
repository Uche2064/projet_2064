from pydantic import BaseModel, EmailStr

from app.model.model import Maison


class BaseUtilisateur(BaseModel):
   nom_complet : str
   email : EmailStr
   cni : str
   numero : str
   adresse : str
   photo : str
   
   class Config:
      from_attributes = True
      
class SchemaUtilisateur(BaseUtilisateur):
   mot_de_passe : str
   
   
class SchemaUtilisateurReponse(BaseUtilisateur):
   id : int
   pass

class TokenData(BaseModel):
   username: str
   id : int
   
   
class SchemaMaison(BaseModel):
   adresse : str
   prix : float
   description : str
   photo : str
   statut : str # à vendre ou à louer
   titre_foncier : bool
   longitude : str
   latitude : str
   utilisateur_id : int
   
class SchemaMaisonUpdate(BaseModel):
   prix : float
   statut : str # à vendre ou à louer
   photo : str
   