from pydantic import BaseModel
from typing import Optional, EmailStr

class CreateUser(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str

class UpdateUser(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
