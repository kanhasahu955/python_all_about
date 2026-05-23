from pydantic import BaseModel


class DataSourceCreate(BaseModel):
    name: str
    provider: str
    host: str | None = None
    port: int | None = None
    username: str | None = None
    password: str | None = None
    database_name: str | None = None
    schema_name: str | None = None
    warehouse: str | None = None
    role: str | None = None
    token: str | None = None
    http_path: str | None = None
    catalog: str | None = None