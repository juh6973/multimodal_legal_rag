from fastapi import FastAPI
import chromadb
import os
from routes.base_routes import router
from utils.logger_config import logger


app = FastAPI()

app.include_router(router, prefix="/api")


@app.get("/")
def read_root():
    logger.info("Backend is running")
    return {"message": "Backend is running"}


# Load ChromaDB client
try:
    client = chromadb.HttpClient(host=os.getenv("CHROMA_HOST"))
    client.delete_collection(os.getenv("CHROMA_MEMORY_COLLECTION"))
    logger.info("ChromaDB client loaded successfully, memory cleaned")
except Exception as e:
    logger.error(f"Error loading ChromaDB client: {e}")

