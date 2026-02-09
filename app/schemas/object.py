from pydantic import BaseModel
from typing import Optional

class CreateObject(BaseModel):
    name: str
    password: str
    user_id: int
    max_temperature: int

class UpdateObject(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    user_id: Optional[int] = None
    max_temperature: Optional[int] = None
