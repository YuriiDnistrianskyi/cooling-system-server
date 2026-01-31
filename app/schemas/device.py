from pydantic import BaseModel
from typing import Optional

class CreateDevice(BaseModel):
    name: str
    password: str
    object_id: int

class UpdateDevice(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    object_id: Optional[int] = None