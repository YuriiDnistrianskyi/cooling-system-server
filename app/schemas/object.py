from pydantic import BaseModel
from typing import Optional

class CreateObject(BaseModel):
    name: str
    password: str
    user_id: int
    max_temperature: float
    default_speed_for_devices: int

class UpdateObject(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    user_id: Optional[int] = None
    max_temperature: Optional[float] = None
    default_speed_for_devices: Optional[int] = None
