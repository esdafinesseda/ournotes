from enum import Enum
from pydantic import BaseModel
from typing import Optional

from app.schemas.index_schema import RecordMeta


class NoteCacheType(Enum):
    DELETE = "delete"
    VALUE = "value"
    META_ONLY = "meta_only"


class NoteCacheUpdate(BaseModel):
    record_id: str
    type: NoteCacheType
    metadata: Optional[dict] = None
    content: Optional[str] = None
