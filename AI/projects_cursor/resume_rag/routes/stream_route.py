from fastapi import APIRouter
from pydantic import BaseModel

from app.streaming.sse import (
    create_llm_stream,
)

router = APIRouter()


class StreamRequest(BaseModel):
    prompt: str


@router.post("/llm")
async def stream_llm(
    request: StreamRequest,
):

    return create_llm_stream(
        request.prompt
    )