from pydantic import BaseModel
from typing import List, Dict, Optional


class RequestMessage(BaseModel):
    message: str

class ResponseMessage(BaseModel):
    status_code: int
    content: str

