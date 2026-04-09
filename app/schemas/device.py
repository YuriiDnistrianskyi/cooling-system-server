from pydantic import BaseModel
from typing import Optional

class CreateDevice(BaseModel):
    public_name: str
    private_name: str
    password: str
    object_id: int

class UpdateDevice(BaseModel):
    public_name: Optional[str] = None
    private_name: Optional[str] = None
    password: Optional[str] = None
    object_id: Optional[int] = None