from app.models.notebook import NotebookModel
from app.services.db.base_service import BaseService


class NotebookService(BaseService):
    def __init__(self):
        super().__init__(model=NotebookModel)
