from typing import Any, Dict, Type, TypeVar
from pydantic import BaseModel

from app.models.asbtract import AbstractModel


ModelType = TypeVar("ModelType", bound=AbstractModel)
CreateSchema = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseService:
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_by_id(self, record_id: int):
        try:
            return await self.model.get(id=record_id)
        except Exception:
            raise

    async def get_all(self):
        return await self.model.all()

    async def create_single(self, create_model: BaseModel):
        try:
            create_data = create_model.model_dump()
            return await self.model.create(**create_data)

        except Exception:
            raise

    async def update_single(self, record_id: int, update_model: BaseModel):
        try:
            record = await self.model.get(id=record_id)

            update_data = update_model.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(record, field, value)

            await record.save()

            return record

        except Exception:
            raise

    async def delete_single(self, record_id: int):
        try:
            record = await self.model.get(id=record_id)
            await record.delete()

            return {"message": "Deleted"}

        except Exception:
            raise
