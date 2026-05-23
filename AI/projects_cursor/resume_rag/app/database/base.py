from abc import ABC, abstractmethod
from typing import Any


class BaseAdapter(ABC):
    def __init__(self, connection_config: dict[str, Any]):
        self.connection_config = connection_config

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

    @abstractmethod
    async def test_connection(self) -> bool:
        pass

    @abstractmethod
    async def get_schemas(self) -> list[str]:
        pass

    @abstractmethod
    async def get_tables(self, schema: str) -> list[str]:
        pass

    @abstractmethod
    async def get_columns(self, schema: str, table: str) -> list[dict]:
        pass

    @abstractmethod
    async def get_primary_keys(self, schema: str, table: str) -> list[str]:
        pass

    @abstractmethod
    async def get_foreign_keys(self, schema: str, table: str) -> list[dict]:
        pass

    @abstractmethod
    async def execute(self, query: str):
        pass

    @abstractmethod
    async def fetch_one(self, query: str):
        pass

    @abstractmethod
    async def fetch_all(self, query: str):
        pass

    @abstractmethod
    async def get_table_count(self, schema: str, table: str) -> int:
        pass

    @abstractmethod
    async def get_sample_data(
        self,
        schema: str,
        table: str,
        limit: int = 100,
    ):
        pass