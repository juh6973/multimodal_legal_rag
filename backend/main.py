from fastapi import FastAPI
from routes.base_routes import router
from utils.logger_config import logger


app = FastAPI()

app.include_router(router, prefix="/api")


@app.get("/")
def read_root():
    logger.info("Backend is running")
    return {"message": "Backend is running"}

