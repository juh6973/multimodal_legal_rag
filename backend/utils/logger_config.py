import logging
from uvicorn.config import LOGGING_CONFIG

# Use Uvicorn's default logging configuration
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("uvicorn.error")