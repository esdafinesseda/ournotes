from pydantic import BaseModel
from typing import Optional


class NotebookCreate(BaseModel):
    title: str
    user_id: int

    class Config:
        from_attributes = True


class NotebookUpdate(BaseModel):
    title: Optional[str] = None
    user_id: Optional[int] = None
