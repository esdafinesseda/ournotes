from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
import uvicorn

from app.config.settings import get_settings
from app.config.database import init_db, close_db
from app.dependencies.services import (
    get_embed_service,
    get_index_service,
    get_user_service,
    get_notebook_service,
    get_topic_service,
    get_note_service,
    get_note_cache_service,
)
from app.routes.note_router import note_router
from app.routes.note_cache_router import note_cache_router
from app.routes.notebook_router import notebook_router
from app.routes.topic_router import topic_router
from app.routes.user_router import user_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(lifespan=lifespan)

app.include_router(
    user_router, prefix=settings.API_V1_STR, dependencies=[Depends(get_user_service)]
)

app.include_router(
    notebook_router,
    prefix=settings.API_V1_STR,
    dependencies=[Depends(get_notebook_service)],
)

app.include_router(
    topic_router, prefix=settings.API_V1_STR, dependencies=[Depends(get_topic_service)]
)

app.include_router(
    note_router,
    prefix=settings.API_V1_STR,
    dependencies=[Depends(get_note_service), Depends(get_note_cache_service)],
)

app.include_router(
    note_cache_router,
    prefix=settings.API_V1_STR,
    dependencies=[Depends(get_note_cache_service)],
)

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
