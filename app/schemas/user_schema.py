from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
