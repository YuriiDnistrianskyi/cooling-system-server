from pydantic import BaseModel
from typing import Optional

class CreateUser(BaseModel):
    firstName: str
    lastName: str
    email: str
    password: str

class UpdateUser(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
