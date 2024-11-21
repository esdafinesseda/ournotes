from pydantic import BaseModel
from typing import Optional

from app.schemas.note_schema import NoteTypeEnum


class RecordMeta(BaseModel):
    user_id: int
    notebook_id: int
    topic_id: int
    note_type: NoteTypeEnum


class IndexRecord(BaseModel):
    id: str
    values: list
    metadata: dict  # dict(IndexMeta)
