from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .jwt import verify_token

#можливо на майбутнє

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

def get_current_user(access_token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_token(access_token)
        return payload.get('user_id')
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)
