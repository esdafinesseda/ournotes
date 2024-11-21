from app.models.user import UserModel
from app.services.db.base_service import BaseService


class UserService(BaseService):
    def __init__(self):
        super().__init__(model=UserModel)
