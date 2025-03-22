from pydantic import BaseModel
from typing import Optional


class OptimizerRequest(BaseModel):
    """Request model for the optimizer"""
    message: str


class OptimizerResponse(BaseModel):
    """Response model for the optimizer"""
    content: str
    status: bool
    error: Optional[str] = None