from fastapi import APIRouter, HTTPException
from models.requests import RequestMessage, ResponseMessage
from models.query_models import OptimizerRequest
from services.query_optimizer import get_optimal_query
from utils.logger_config import logger


router = APIRouter()


@router.post("/test")
def test_connection(request: RequestMessage):
    """Test connection to backend"""
    print("Connection successful")
    print(request.message)
    return ResponseMessage(status_code=200, content="Connection successful")


@router.post("/optimizer")
def optimize_query(request: RequestMessage):
    """Optimize query for retrieval tasks"""
    logger.info(f"Request received: {request.message}")
    try:
        # Optimize query
        optimized_query = get_optimal_query(OptimizerRequest(message=request.message))
        logger.info(f"Optimized query generated: {optimized_query.content}")
        return ResponseMessage(status_code=200, content=optimized_query.content)
    except Exception as e:
        logger.error(f"Error optimizing query: {e}")
        raise HTTPException(status_code=500, detail="Error optimizing query")


@router.post("/generate")
def generate_response(request: RequestMessage):
    """Generate optimal query for retrieval tasks"""
    logger.info(f"Request received: {request.message}")
    
    return ResponseMessage(status_code=200, content="Response generated")
