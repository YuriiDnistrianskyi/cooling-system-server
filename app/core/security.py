from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
)

def hash_password(password: str) -> str:
    hashed = pwd_context.hash(password)
    return hashed

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)
