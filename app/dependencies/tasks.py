from fastapi import Depends
from typing import Annotated

from app.tasks.index_update import IndexUpdate
from app.dependencies.services import (
    EmbedServiceDep,
    IndexServiceDep,
    NoteCacheServiceDep,
)


def get_update_task(
    embed_service: EmbedServiceDep,
    index_service: IndexServiceDep,
    note_cache_service: NoteCacheServiceDep,
) -> IndexUpdate:
    return IndexUpdate(
        embed_service=embed_service,
        index_service=index_service,
        note_cache_service=note_cache_service,
    )


UpdateTaskDep = Annotated[IndexUpdate, Depends(get_update_task)]
