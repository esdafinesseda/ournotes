from pydantic import BaseModel


class NotebookCreate(BaseModel):
    title: str
    user_id: int

    class Config:
        from_attributes = True
