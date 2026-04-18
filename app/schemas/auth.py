from pydantic import BaseModel

class Login(BaseModel):
    email: str
    password: str

class Refresh(BaseModel):
    refresh_token: str
