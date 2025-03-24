from fastapi import APIRouter, HTTPException
from models.requests import RequestMessage, ResponseMessage
from models.query_models import OptimizerRequest, RagResponse, OptimizerResponse
from services.query_optimizer import get_optimal_query
from services.rag import query_rag
from services.formatter_model import format_response, format_context
from utils.logger_config import logger
import time


router = APIRouter()


@router.post("/test")
def test_connection(request: RequestMessage):
    """Test connection to backend"""
    print("Connection successful")
    print(request.message)
    return ResponseMessage(status_code=200, content="Connection successful")


@router.post("/test-format")
def format_res(request: RequestMessage):
    """Format response from the model"""
    logger.info(f"Request received: {request.message}")
    formatted_response = format_response(request.message)
    logger.info(f"Formatted response generated: {formatted_response}")

    return ResponseMessage(status_code=200, content=formatted_response)


@router.post("/generate")
def generate_response(request: RequestMessage):
    """Optimize query for retrieval tasks"""
    start_time = time.time()
    logger.info(f"Request received: {request.message}")
    #try:
    # Optimize query
    optimized_query = get_optimal_query(
        request=OptimizerRequest(message=request.message)
        )
    logger.info(f"Optimized query generated: {optimized_query.content}")

    rag_response = query_rag(query=optimized_query.content)
    logger.info(f"RAG response generated: {rag_response.content}")

    formatted_context = format_context(documents=rag_response)
    logger.info(f"Formatted context generated: {formatted_context}")

    response = format_response(
        user_query=request.message, 
        legal_context=formatted_context,
        )
    logger.info(f"Formatted response generated: {response}")

    logger.info(f"Time taken: {time.time() - start_time}")

    return ResponseMessage(status_code=200, content=response)
    #except Exception as e:
    #    logger.error(f"Error optimizing query: {e}")
    #    raise HTTPException(status_code=500, detail="Error optimizing query")


@router.post("/test-query")
def optimize_query(request: RequestMessage):
    """Generate optimal query for retrieval tasks"""
    logger.info(f"Request received: {request.message}")
    optimal_query = get_optimal_query(OptimizerRequest(message=request.message))
    logger.info(f"Optimized query generated: {optimal_query.content}")

    return ResponseMessage(status_code=200, content=optimal_query.content)
