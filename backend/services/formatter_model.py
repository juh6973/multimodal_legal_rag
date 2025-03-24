import os
import time

from langchain.prompts import PromptTemplate

from models.query_models import RagResponse
from models.requests import ResponseMessage
from services.query_optimizer import get_hf_model
from utils.logger_config import logger
from utils.prompts import FORMATTER_PROMPT, FORMATTER_PROMPT_TEST


def format_context(documents: RagResponse) -> str:
    """Format the context to a str list for the model"""
    
    # Get the context
    formatted_context = [f"Case {i}:\nContext: {doc.content}\nMetadata: {doc.meta_data}\n{"-"*10}" for i, doc in enumerate(documents.content)]

    return "\n".join(formatted_context)


def parse_deepseek(response: str) -> str:
    """Parse the response from the deepseek model"""
    return response.split("</think>")[1].strip()


def format_response(user_query:str, legal_context:str) -> str:
    """Format the response from the model"""
    try:

        # Get the model
        #model_name = "Juh6973/DeepSeek-R1-Legal-Advice-COT"
        model_name = "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"
        llm = get_hf_model(
            model_name=model_name, 
            quantization=True,
            max_new_tokens=3000,
            )

        # Get the prompt
        prompt = PromptTemplate.from_template(template=FORMATTER_PROMPT)

        # Define the chain
        chain = prompt | llm

        # Invoke the chain
        start_time = time.time()
        response = chain.invoke({"legal_context": legal_context, "query": user_query})
        end_time = time.time() - start_time

        if os.getenv("DEBUG"):
            logger.info(f"Response: {response}")
            logger.info(f"Time taken to generate response: {end_time}")


        # Parse the response if using a DeepSeek model
        if "deepseek" in model_name.lower():
            response = parse_deepseek(response)

        return response


    except Exception as e:
        logger.error(f"Error formatting response: {e}")
        return ResponseMessage(status_code=500, content="Error in formatter model response")

    