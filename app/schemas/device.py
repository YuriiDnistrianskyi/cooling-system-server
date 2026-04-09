from pydantic import BaseModel
from typing import Optional

class CreateDevice(BaseModel):
    publicName: str
    privateName: str
    password: str
    object_id: int

class UpdateDevice(BaseModel):
    publicName: Optional[str] = None
    privateName: Optional[str] = None
    password: Optional[str] = None
    object_id: Optional[int] = None