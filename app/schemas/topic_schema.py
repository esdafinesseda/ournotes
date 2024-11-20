from pydantic import BaseModel
from typing import Optional


class TopicCreate(BaseModel):
    title: str
    notebook_id: int
    parent_id: Optional[int] = None

    class Config:
        from_attributes = True
