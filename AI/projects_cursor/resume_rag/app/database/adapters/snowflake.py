from sqlalchemy import create_engine, text
from database.base import BaseAdapter

class SnowflakeAdapter(BaseAdapter):
    async def connect(self):
        self.engine = create_engine(
            self.connection_config["url"]
        )
        return self.engine

    async def disconnect(self):
        self.engine.dispose()

    async def test_connection(self):
        with self.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True

    async def get_schemas(self):
        with self.engine.connect() as conn:
            result = conn.execute(
                text("SHOW SCHEMAS")
            )
            return [row[1] for row in result]