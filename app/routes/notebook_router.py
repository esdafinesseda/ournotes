from fastapi import APIRouter


from app.schemas.notebook_schema import NotebookCreate, NotebookUpdate
from app.dependencies.services import NotebookServiceDep

notebook_router = APIRouter(prefix="/notebooks")


@notebook_router.get("/{notebook_id}")
async def get_notebook(notebook_id: int, notebook_service: NotebookServiceDep):
    return await notebook_service.get_by_id(notebook_id)


@notebook_router.get("/")
async def get_all_notebooks(notebook_service: NotebookServiceDep):
    return await notebook_service.get_all()


@notebook_router.post("/")
async def create_notebook(
    notebook_create: NotebookCreate, notebook_service: NotebookServiceDep
):
    return await notebook_service.create_single(notebook_create)


@notebook_router.put("/{notebook_id}")
async def update_notebook(
    notebook_id: int,
    notebook_update: NotebookUpdate,
    notebook_service: NotebookServiceDep,
):
    return await notebook_service.update_single(notebook_id, notebook_update)


@notebook_router.delete("/{notebook_id}")
async def delete_notebook(notebook_id: int, notebook_service: NotebookServiceDep):
    return await notebook_service.delete_single(notebook_id)
