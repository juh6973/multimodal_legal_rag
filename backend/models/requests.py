from pydantic import BaseModel
from typing import List, Dict, Optional


class RequestMessage(BaseModel):
    prompt: str
    message_history: List[Dict[str, str]]


class ResponseMessage(BaseModel):
    status_code: int
    content: str

