from fastapi import Depends
from functools import lru_cache
from typing import Annotated

from app.config.settings import Settings, get_settings
from app.services.embed_service import EmbedService
from app.services.index_service import IndexService
from app.services.db.user_service import UserService
from app.services.db.notebook_service import NotebookService
from app.services.db.topic_service import TopicService
from app.services.db.note_service import NoteService
from app.services.db.note_cache_service import NoteCacheService


def get_embed_service(settings: Settings = Depends(get_settings)) -> EmbedService:
    return EmbedService()


async def get_index_service(settings: Settings = Depends(get_settings)) -> IndexService:
    index_service = IndexService()
    await index_service.create()
    return index_service


def get_user_service() -> UserService:
    return UserService()


def get_notebook_service() -> NotebookService:
    return NotebookService()


def get_topic_service() -> TopicService:
    return TopicService()


def get_note_service() -> NoteService:
    return NoteService()


def get_note_cache_service() -> NoteCacheService:
    return NoteCacheService()


# Depdency annoations
EmbedServiceDep = Annotated[EmbedService, Depends(get_embed_service)]
IndexServiceDep = Annotated[IndexService, Depends(get_index_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
NotebookServiceDep = Annotated[NotebookService, Depends(get_notebook_service)]
TopicServiceDep = Annotated[TopicService, Depends(get_topic_service)]
NoteServiceDep = Annotated[NoteService, Depends(get_note_service)]
NoteCacheServiceDep = Annotated[NoteCacheService, Depends(get_note_cache_service)]
