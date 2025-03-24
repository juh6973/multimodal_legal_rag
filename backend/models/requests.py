from pydantic import BaseModel
from typing import List, Dict, Optional


class RequestMessage(BaseModel):
    prompt: str
    message_history: List[Dict[str, str]]
    context: Optional[str] = None


class ResponseMessage(BaseModel):
    status_code: int
    content: str
    context: Optional[str] = None

