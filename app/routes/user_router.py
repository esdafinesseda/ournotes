from fastapi import APIRouter


from app.schemas.user_schema import UserCreate, UserUpdate
from app.dependencies.services import UserServiceDep

user_router = APIRouter(prefix="/users")


@user_router.get("/{user_id}")
async def get_user(user_id: int, user_service: UserServiceDep):
    return await user_service.get_by_id(user_id)


@user_router.get("/")
async def get_all_users(user_service: UserServiceDep):
    return await user_service.get_all()


@user_router.post("/")
async def create_user(user_create: UserCreate, user_service: UserServiceDep):
    return await user_service.create_single(user_create)


@user_router.put("/{user_id}")
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    user_service: UserServiceDep,
):
    return await user_service.update_single(user_id, user_update)


@user_router.delete("/{user_id}")
async def delete_user(user_id: int, user_service: UserServiceDep):
    return await user_service.delete_single(user_id)
