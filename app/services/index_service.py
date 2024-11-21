from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

from pinecone import Pinecone, ServerlessSpec
from pinecone.exceptions import PineconeException
from typing import List

from app.config.settings import get_settings


class IndexService:
    def __init__(self):
        self.settings = get_settings()
        self.pc = Pinecone(api_key=self.settings.PC_API_KEY)
        self.spec = ServerlessSpec(
            cloud=self.settings.PC_CLOUD, region=self.settings.PC_REGION
        )

    async def create(self):
        await self.create_index(self.settings.PC_INDEX_NAME)

    @retry(
        stop=stop_after_attempt(5),  # Retry up to 5 times
        wait=wait_exponential(multiplier=1, min=1, max=10),  # Back off
        retry=retry_if_exception_type(PineconeException),
        reraise=True,  # Raise last exception
    )
    async def index_ready(self, index_name: str) -> None:
        index_status = self.pc.describe_index(index_name)

        if not index_status["status"]["ready"]:
            raise PineconeException(f"Index {index_name} not ready!")

    async def create_index(self, index_name: str) -> None:
        try:
            if not self.pc.has_index(index_name):
                self.pc.create_index(
                    name=index_name,
                    dimension=self.settings.EMB_DIM,
                    metric=self.settings.PC_METRIC,
                    spec=self.spec,
                )

            await self.index_ready(index_name)

        except PineconeException:
            raise

        self.index = self.pc.Index(index_name)

    async def search_index(self, query_vector: list, filter: dict, top_k: int):
        results = await self.index.query(
            vector=query_vector, filter=filter, top_k=top_k, include_metadata=True
        )

        return results

    async def delete_index(self, index_name: str):
        self.pc.delete_index(index_name)

    async def add_record(self, index_record: dict):
        self.index.upsert([index_record])

    def add_records(self, index_records: List[dict]):
        self.index.upsert(index_records)

    async def update_record_meta(self, record_id: str, update_meta: dict):
        self.index.update(id=record_id, set_metadata=update_meta)

    async def update_record_value(self, record_id: str, values: list):
        self.index.update(id=record_id, values=values)

    async def delete_record(self, record_id):
        self.index.delete(ids=[record_id])

    async def delete_records(self, index_ids: List[int]):
        self.index.delete(ids=index_ids)
