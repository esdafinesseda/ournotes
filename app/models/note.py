from tortoise import fields

from app.models.asbtract import AbstractModel
from app.schemas.note_schema import NoteTypeEnum


class NoteModel(AbstractModel):
    type = fields.CharEnumField(enum_type=NoteTypeEnum)
    content = fields.TextField()

    # Relationships
    topic = fields.ForeignKeyField(
        "models.TopicModel", related_name="notes", on_delete=fields.CASCADE
    )

    class Meta:
        table = "notes"
