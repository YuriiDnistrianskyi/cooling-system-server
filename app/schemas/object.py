from pydantic import BaseModel
from typing import Optional

class CreateObject(BaseModel):
    name: str
    password: str
    user_id: int

class UpdateObject(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    user_id: Optional[int] = None
