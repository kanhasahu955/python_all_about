from typing import Optional
from sqlmodel import SQLModel, Field


class AgentRun(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    document_id: str = Field(index=True)
    agent_name: str
    status: str
    input_json: Optional[str] = None
    output_json: Optional[str] = None