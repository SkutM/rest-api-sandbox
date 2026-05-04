from pydantic import BaseModel
from typing import Optional

class EchoRequest(BaseModel):
    message: str
    times: int

class UserCreate(BaseModel):
    name: str

class UserResponse(BaseModel):
    id: int
    name: str

class UserUpdate(BaseModel):
    name: Optional[str] = None