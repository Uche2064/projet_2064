from fastapi import APIRouter

route = APIRouter(
   tags=["Annonce"],
   prefix="/annonce"
)

@route.get("/")
async def get_offres():
   return {"data" : "annonces"}