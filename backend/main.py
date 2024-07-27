from fastapi import FastAPI
from app.routes import auth, annonce, maison, utilisateur, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],  # Adjust according to your requirements
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)

app.include_router(utilisateur.router)
# app.include_router(offre.route)
# app.include_router(annonce.route)
app.include_router(maison.router)