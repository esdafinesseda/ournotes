from enum import Enum
from pydantic import BaseModel

from app.schemas.note_schema import NoteTypeEnum


class NoteTypeEnum(str, Enum):
    general = "general"
    definition = "definition"
    example = "example"
    question = "question"
    answer = "answer"


class NoteCreate(BaseModel):
    type: NoteTypeEnum = NoteTypeEnum.general
    content: str
    topic_id: int

    class Config:
        from_attributes = True
