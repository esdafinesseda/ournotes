from fastapi import APIRouter


from app.schemas.topic_schema import TopicCreate, TopicUpdate
from app.dependencies.services import TopicServiceDep

topic_router = APIRouter(prefix="/topics")


@topic_router.get("/{topic_id}")
async def get_topic(topic_id: int, topic_service: TopicServiceDep):
    return await topic_service.get_by_id(topic_id)


@topic_router.get("/")
async def get_all_topics(topic_service: TopicServiceDep):
    return await topic_service.get_all()


@topic_router.post("/")
async def create_topic(topic_create: TopicCreate, topic_service: TopicServiceDep):
    return await topic_service.create_single(topic_create)


@topic_router.put("/{topic_id}")
async def update_topic(
    topic_id: int,
    topic_update: TopicUpdate,
    topic_service: TopicServiceDep,
):
    return await topic_service.update_single(topic_id, topic_update)


@topic_router.delete("/{topic_id}")
async def delete_topic(topic_id: int, topic_service: TopicServiceDep):
    return await topic_service.delete_single(topic_id)
