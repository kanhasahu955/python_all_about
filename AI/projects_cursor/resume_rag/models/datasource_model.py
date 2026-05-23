from typing import Optional
from sqlmodel import SQLModel, Field


class DataSource(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    provider: str = Field(index=True)
    host: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    database_name: Optional[str] = None
    schema_name: Optional[str] = None
    warehouse: Optional[str] = None
    role: Optional[str] = None
    token: Optional[str] = None
    http_path: Optional[str] = None
    catalog: Optional[str] = None
    is_active: bool = True