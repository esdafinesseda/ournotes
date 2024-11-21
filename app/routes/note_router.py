from fastapi import APIRouter

from app.schemas.note_schema import NoteCreate, NoteUpdateContent, NoteUpdateMeta
from app.dependencies.services import (
    NoteServiceDep,
    NoteCacheServiceDep,
)

note_router = APIRouter(prefix="/notes")


@note_router.get("/{note_id}")
async def get_note(note_id: int, note_service: NoteServiceDep):
    return await note_service.get_by_id(note_id)


@note_router.get("/")
async def get_all_notes(note_service: NoteServiceDep):
    return await note_service.get_all()


@note_router.post("/")
async def create_note(
    note_create: NoteCreate,
    note_service: NoteServiceDep,
    note_cache_service: NoteCacheServiceDep,
):
    note, cache_update = await note_service.create_single(note_create)
    await note_cache_service.create_upsert_or_delete(cache_update)

    return note


@note_router.put("/meta/{note_id}")
async def update_note_meta(
    note_id: int,
    note_update: NoteUpdateMeta,
    note_service: NoteServiceDep,
    note_cache_service: NoteCacheServiceDep,
):
    note, cache_update = await note_service.update_single_meta(note_id, note_update)
    await note_cache_service.create_meta_only(cache_update)

    return note


@note_router.put("/content/{note_id}")
async def update_note_meta(
    note_id: int,
    note_update: NoteUpdateContent,
    note_service: NoteServiceDep,
    note_cache_service: NoteCacheServiceDep,
):
    note, cache_update = await note_service.update_single_value(note_id, note_update)
    await note_cache_service.create_upsert_or_delete(cache_update)

    return note


@note_router.delete("/{note_id}")
async def delete_note(
    note_id: int, note_service: NoteServiceDep, note_cache_service: NoteCacheServiceDep
):
    delete, cache_update = await note_service.delete_single(note_id)
    await note_cache_service.create_upsert_or_delete(cache_update)

    return delete
