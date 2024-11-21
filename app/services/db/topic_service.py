from app.models.topic import TopicModel
from app.services.db.base_service import BaseService


class TopicService(BaseService):
    def __init__(self):
        super().__init__(model=TopicModel)
