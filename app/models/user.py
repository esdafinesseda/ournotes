from tortoise import fields

from app.models.asbtract import AbstractModel


class UserModel(AbstractModel):
    username = fields.CharField(max_length=150, unique=True)
    email = fields.CharField(max_length=255, unique=True)

    class Meta:
        table = "users"
