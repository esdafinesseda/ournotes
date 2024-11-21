from tortoise import fields

from app.models.asbtract import AbstractModel


class TopicModel(AbstractModel):
    title = fields.CharField(max_length=100)

    # Relationships
    notebook = fields.ForeignKeyField(
        "models.NotebookModel", related_name="notes", on_delete=fields.CASCADE
    )
    # For subtopics
    parent = fields.ForeignKeyField(
        "models.TopicModel",
        related_name="subtopics",
        null=True,
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = "topics"
