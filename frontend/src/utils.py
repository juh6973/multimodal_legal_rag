import os
import requests
import base64
from io import BytesIO
from PIL import Image

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
    

def convert_to_base64(pil_image):
    """Convert PIL images to Base64 encoded strings"""

    # Convert PIL image to BytesIO object
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    # Convert to a Base64
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str


def convert_image(image: str):
    """Convert uploaded image to Base64 string"""

    image = Image.open(image)

    # Convert to a Base64
    img_base64 = convert_to_base64(image)
    return img_base64
        