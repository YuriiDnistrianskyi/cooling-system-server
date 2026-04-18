from pydantic import BaseModel
from typing import Optional

class CreateDevice(BaseModel):
    publicName: str
    privateName: str
    password: str
    objectId: int

class UpdateDevice(BaseModel):
    publicName: Optional[str] = None
    privateName: Optional[str] = None
    password: Optional[str] = None
    objectId: Optional[int] = None