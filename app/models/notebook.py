from tortoise import fields

from app.models.asbtract import BaseModel


class NotebookModel(BaseModel):
    title = fields.CharField(max_length=100)

    # Relationships
    user = fields.ForeignKeyField(
        "models.UserModel", related_name="notebooks", on_delete=fields.CASCADE
    )

    class Meta:
        table = "notebooks"