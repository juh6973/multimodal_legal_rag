from fastapi import APIRouter, HTTPException
from models.requests import RequestMessage, ResponseMessage
from models.query_models import OptimizerRequest, RagResponse, OptimizerResponse
from services.query_optimizer import get_optimal_query
from services.rag import query_rag
from services.formatter_model import format_response, format_context
from services.conversation import chat_model
from utils.logger_config import logger
import time


router = APIRouter()


@router.post("/test")
def test_connection(request: RequestMessage):
    """Test connection to backend"""
    print("Connection successful")
    print(request.prompt)
    return ResponseMessage(status_code=200, content="Connection successful")


@router.post("/test-format")
def format_res(request: RequestMessage):
    """Format response from the model"""
    logger.info(f"Request received: {request.prompt}")
    formatted_response = format_response(request.prompt)
    logger.info(f"Formatted response generated: {formatted_response}")

    return ResponseMessage(status_code=200, content=formatted_response)


@router.post("/generate")
def generate_response(request: RequestMessage):
    """Optimize query for retrieval tasks, Error handling is done in deeper layers"""

    start_time = time.time()
    logger.info(f"Request received: {request.prompt}")
    logger.info(f"Messages received: {len(request.message_history)}")
    logger.info(f"Context size: {len(request.context)}")
    
    # first message runs retrieval and formatting tasks
    if len(request.message_history) == 1:
        # Optimize query
        optimized_query = get_optimal_query(
            request=OptimizerRequest(message=request.prompt)
            )
        logger.info(f"Optimized query generated")

        # Query RAG
        rag_response = query_rag(query=optimized_query.content)
        logger.info(f"RAG response generated")

        # Format rag response
        formatted_context = format_context(documents=rag_response)
        context = formatted_context
        logger.info(f"Formatted context generated")

        # Formatter model
        response = format_response(
            user_query=request.prompt, 
            legal_context=formatted_context,
            )

    # latter messages runs conversation model
    else:
        context = request.context
        response = chat_model(
            prompt=request.prompt,
            messages=request.message_history,
            context=context,
            )
        
    logger.info(f"Response generated: {response}")
    logger.info(f"Time taken: {time.time() - start_time}")

    # Return response
    return ResponseMessage(status_code=200, content=response, context=context)


@router.post("/test-query")
def optimize_query(request: RequestMessage):
    """Generate optimal query for retrieval tasks"""
    logger.info(f"Request received: {request.prompt}")
    optimal_query = get_optimal_query(OptimizerRequest(message=request.prompt))
    logger.info(f"Optimized query generated: {optimal_query.content}")

    return ResponseMessage(status_code=200, content=optimal_query.content)
