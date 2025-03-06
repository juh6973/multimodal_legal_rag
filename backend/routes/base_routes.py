import os
import requests
from fastapi import APIRouter, HTTPException
from models.requests import RequestMessage, ResponseMessage

router = APIRouter()

@router.post("/test")
def test_connection(request: RequestMessage):
    """Test connection to backend"""
    print("Connection successful")
    print(request.message)
    return ResponseMessage(status_code=200, content="Connection successful")

