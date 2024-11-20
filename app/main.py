from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI

from app.config.settings import get_settings
from app.config.database import init_db, close_db

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
