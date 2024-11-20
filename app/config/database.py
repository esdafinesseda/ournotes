from tortoise import Tortoise

from app.config.settings import get_settings

settings = get_settings()


async def init_db():
    await Tortoise.init(
        db_url=settings.DB_URL,
        modules={
            "models": [
                "app.models.user",
                "app.models.note",
                "app.models.notebook",
                "app.models.topic",
            ]
        },
    )

    await Tortoise.generate_schemas()


async def close_db():
    await Tortoise.close_connections()
