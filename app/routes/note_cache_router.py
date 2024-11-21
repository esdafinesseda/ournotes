from fastapi import APIRouter


from app.dependencies.services import NoteCacheServiceDep
from app.dependencies.tasks import UpdateTaskDep

note_cache_router = APIRouter(prefix="/note_caches")


@note_cache_router.get("/")
async def get_all_note_caches(note_cache_service: NoteCacheServiceDep):
    return await note_cache_service.get_all()


@note_cache_router.get("/update")
async def update_index(update_task: UpdateTaskDep):
    return await update_task.update_index()
