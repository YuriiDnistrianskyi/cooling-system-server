from pydantic import BaseModel
from typing import Optional

class CreateObject(BaseModel):
    publicName: str
    privateName: str
    password: str
    userId: int
    maxTemperature: float
    defaultSpeedForDevices: int

class UpdateObject(BaseModel):
    publicName: Optional[str] = None
    privateName: Optional[str] = None
    password: Optional[str] = None
    userId: Optional[int] = None
    maxTemperature: Optional[float] = None
    defaultSpeedForDevices: Optional[int] = None
