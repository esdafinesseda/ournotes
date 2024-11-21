from typing import Any, Dict
from tortoise.exceptions import DoesNotExist

from app.models.note_cache import NoteCacheModel
from app.schemas.note_cache_schema import NoteCacheUpdate
from app.services.db.base_service import BaseService


class NoteCacheService(BaseService):
    def __init__(self):
        super().__init__(model=NoteCacheModel)

    async def create_meta_only(self, cache_update: NoteCacheUpdate):
        try:
            last: NoteCacheModel = await self.model.get(
                record_id=cache_update.record_id
            )
            last.metadata = cache_update.metadata
            await last.save()

            return last

        except DoesNotExist:
            return await self.create_single(cache_update)

    async def create_upsert_or_delete(self, update_value: NoteCacheUpdate):
        await self.model.filter(record_id=update_value.record_id).delete()

        return await self.create_single(update_value)

    async def clear(self):
        await self.model.all().delete()
