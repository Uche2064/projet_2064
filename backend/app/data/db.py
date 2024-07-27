from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.settings import setting

SQLALCHEMY_DATABASE_URL = f"mysql://{setting.db_user}:{setting.db_password}@{setting.db_host}:{setting.db_port}/{setting.db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
   db = SessionLocal()
   try:
      yield db
   finally:
      db.close()