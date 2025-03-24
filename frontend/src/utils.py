import os
import requests


def send_request(path: str, data: dict):
    """Send request to backend"""
    try:
        response = requests.post(
            os.getenv("BACKEND_URL") + path, 
            json=data
            )
        
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}
