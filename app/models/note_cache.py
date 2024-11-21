from tortoise import fields

from app.models.asbtract import AbstractModel
from app.schemas.note_cache_schema import NoteCacheType


class NoteCacheModel(AbstractModel):
    record_id = fields.CharField(max_length=20)
    type = fields.CharEnumField(enum_type=NoteCacheType)
    metadata = fields.JSONField(null=True)
    content = fields.TextField(null=True)

    class Meta:
        table = "index_note_cache"
