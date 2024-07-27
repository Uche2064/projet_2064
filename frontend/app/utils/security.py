from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(secret: str) -> str:
   return pwd_context.hash(secret)


def verify_password(secret: str, hash: str) -> bool:
   return pwd_context.verify(secret, hash)
