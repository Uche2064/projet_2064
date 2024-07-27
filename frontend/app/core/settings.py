from pydantic_settings import BaseSettings


class Settings(BaseSettings):
   db_name: str
   db_port: int
   db_host: str
   db_user: str
   db_password: str
   secret_key: str
   algorithm: str
   duree_acces: int
   
   class Config:
      env_file = ".env"

setting = Settings()