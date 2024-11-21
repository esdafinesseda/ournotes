from typing import List

from app.models.note_cache import NoteCacheModel
from app.schemas.index_schema import RecordMeta, IndexRecord
from app.schemas.note_cache_schema import NoteCacheType
from app.services.embed_service import EmbedService
from app.services.index_service import IndexService
from app.services.db.note_cache_service import NoteCacheService


class IndexUpdate:
    def __init__(
        self,
        embed_service: EmbedService,
        index_service: IndexService,
        note_cache_service: NoteCacheService,
    ):
        self.embed_service = embed_service
        self.index_service = index_service
        self.note_cache_service = note_cache_service
        self.upserts = []
        self.updates = []
        self.deletes = []

    async def _populate_records(self):
        updates: List[NoteCacheModel] = await self.note_cache_service.get_all()

        for update in updates:
            if update.type == NoteCacheType.DELETE:
                self.deletes.append(update.record_id)

            elif update.type == NoteCacheType.VALUE:
                values = self.embed_service.generate_embedding(update.content)

                upsert_record = IndexRecord(
                    id=update.record_id, values=values, metadata=update.metadata
                ).model_dump()

                self.upserts.append(upsert_record)

            elif update.type == NoteCacheType.META_ONLY:
                self.updates.append((update.record_id, update.metadata))

        print(len(self.upserts))
        print(len(self.deletes))
        print(len(self.updates))

    async def _deletes(self, batch_size: int = 100):
        if not self.deletes:
            return

        for i in range(0, len(self.deletes), batch_size):
            batch = self.deletes[i : i + batch_size]
            try:
                self.index_service.delete_records(batch)
            except Exception:
                raise

    async def _upserts(self, batch_size: int = 100):
        if not self.upserts:
            return

        for i in range(0, len(self.upserts), batch_size):
            batch = self.upserts[i : i + batch_size]

            try:
                self.index_service.add_records(batch)

            except Exception:
                raise

    async def _updates(self):
        if not self.updates:
            return

        for update in self.updates:
            record_id, metadata = update

            self.index_service.update_record_meta(record_id, metadata)

    async def update_index(self):
        await self._populate_records()
        await self._deletes()
        await self._upserts()
        await self._updates()

        await self.note_cache_service.clear()

        return {"message": "Index Updated Cache Cleared"}
