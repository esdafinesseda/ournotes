from enum import Enum
from pydantic import BaseModel
from typing import Optional


class NoteTypeEnum(str, Enum):
    GENERAL = "general"
    DEFINITION = "definition"
    EXAMPLE = "example"
    QUESTION = "question"
    ANSWER = "answer"


class NoteCreate(BaseModel):
    type: NoteTypeEnum
    content: str
    topic_id: int

    class Config:
        from_attributes = True


class NoteUpdateMeta(BaseModel):
    type: Optional[NoteTypeEnum] = None
    topic_id: Optional[int] = None


class NoteUpdateContent(BaseModel):
    content: str
