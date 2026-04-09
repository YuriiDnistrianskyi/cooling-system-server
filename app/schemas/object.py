from pydantic import BaseModel
from typing import Optional

class CreateObject(BaseModel):
    publicName: str
    privateName: str
    password: str
    user_id: int
    max_temperature: float
    default_speed_for_devices: int

class UpdateObject(BaseModel):
    publicName: Optional[str] = None
    privateName: Optional[str] = None
    password: Optional[str] = None
    user_id: Optional[int] = None
    max_temperature: Optional[float] = None
    default_speed_for_devices: Optional[int] = None
