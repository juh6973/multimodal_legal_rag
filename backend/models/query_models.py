from pydantic import BaseModel
from typing import List, Optional


class OptimizerRequest(BaseModel):
    """Request model for the optimizer"""
    message: str


class OptimizerResponse(BaseModel):
    """Response model for the optimizer"""
    content: str
    status: bool
    error: Optional[str] = None


class Document(BaseModel):
    """Document model for the RAG model"""
    content: str
    id: str
    meta_data: Optional[dict]


class RagResponse(BaseModel):
    """Response model for the RAG model"""
    content: List[Document]
    score: List[float]