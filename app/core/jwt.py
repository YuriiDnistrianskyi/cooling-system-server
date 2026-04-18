from fastapi import HTTPException, status
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from .config import SECRET_KEY


def create_access_token(user_id: int):
    encode = {
        'user_id': user_id
    }
    expire = datetime.now(timezone.utc) + timedelta(minutes=5)
    encode.update({'exp': expire})
    return jwt.encode(encode, SECRET_KEY, algorithm='HS256')

def create_refresh_token(user_id: int):
    encode = {
        'user_id': user_id
    }
    expire = datetime.now(timezone.utc) + timedelta(days=10)
    encode.update({'exp': expire})
    return jwt.encode(encode, SECRET_KEY, algorithm='HS256')

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Signature expired. Please log in again.'
        )
