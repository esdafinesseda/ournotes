from pydantic import BaseModel
from app.models.note import NoteModel
from app.models.notebook import NotebookModel
from app.models.topic import TopicModel
from app.models.user import UserModel
from app.schemas.index_schema import RecordMeta
from app.schemas.note_cache_schema import NoteCacheType, NoteCacheUpdate
from app.schemas.note_schema import NoteUpdateMeta, NoteUpdateContent
from app.services.db.base_service import BaseService


class NoteService(BaseService):
    def __init__(self):
        super().__init__(model=NoteModel)

    async def generate_record_meta(self, note: NoteModel) -> dict:
        topic: TopicModel = await note.topic
        notebook: NotebookModel = await topic.notebook
        user: UserModel = await notebook.user

        metadata = RecordMeta(
            user_id=user.id,
            notebook_id=notebook.id,
            topic_id=topic.id,
            note_type=note.type,
        )

        return metadata.model_dump()

    async def create_single(self, create_model: BaseModel):
        note: NoteModel = await super().create_single(create_model)
        metadata = await self.generate_record_meta(note)
        cache_update = NoteCacheUpdate(
            record_id=str(note.id),
            type=NoteCacheType.VALUE,
            metadata=metadata,
            content=note.content,
        )

        print(f"Content: {note.content}")

        return note, cache_update

    async def update_single_meta(self, note_id: int, update_meta_model: NoteUpdateMeta):
        note: NoteModel = await self.model.get(id=note_id)

        # If topic supplied, update note model
        if update_meta_model.topic_id:
            note.topic = await TopicModel.get(id=update_meta_model.topic_id)

        if update_meta_model.type:
            note.type = update_meta_model.type

        await note.save()

        metadata = await self.generate_record_meta(note)

        cache_update = NoteCacheUpdate(
            record_id=str(note.id), type=NoteCacheType.META_ONLY, metadata=metadata
        )

        return note, cache_update

    async def update_single_value(self, note_id: int, value_update: NoteUpdateContent):
        note: NoteModel = await self.model.get(id=note_id)
        note.content = value_update.content
        await note.save()

        metadata = await self.generate_record_meta(note)

        cache_update = NoteCacheUpdate(
            record_id=str(note.id),
            type=NoteCacheType.VALUE,
            metadata=metadata,
            content=note.content,
        )

        return note, cache_update

    async def delete_single(self, record_id: int):
        delete = await super().delete_single(record_id)

        cache_update = NoteCacheUpdate(
            record_id=str(record_id), type=NoteCacheType.DELETE
        )

        return delete, cache_update
