from tortoise import fields

from app.models.asbtract import BaseModel
from app.schemas.note_schema import NoteTypeEnum


class NoteModel(BaseModel):
    type = fields.CharEnumField(
        enum_type=NoteTypeEnum, default=NoteTypeEnum.general, description="Note Type"
    )
    content = fields.TextField()

    # Relationships
    notebook = fields.ForeignKeyField(
        "models.TopicModel", related_name="notes", on_delete=fields.CASCADE
    )

    class Meta:
        table = "notes"
