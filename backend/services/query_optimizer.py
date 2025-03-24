import json
import os
import re
import time

from langchain_huggingface import  HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.globals import set_verbose, set_debug

from transformers import BitsAndBytesConfig
from huggingface_hub.commands.user import login

from models.query_models import OptimizerRequest, OptimizerResponse
from models.requests import ResponseMessage
from utils.logger_config import logger
from utils.prompts import OPTIMIZER_PROMPT


def get_hf_model(
        model_name: str = "mistralai/Mistral-7B-Instruct-v0.3", 
        quantization=True,
        max_new_tokens=2048,
        ) -> HuggingFacePipeline: 
    # "HuggingFaceH4/zephyr-7b-beta" 
    # "mistralai/Mistral-7B-Instruct-v0.3" 
    # "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"
    """Get the model from the Hugging Face model hub"""

    # Login to Hugging Face
    login(token=os.getenv("HF_TOKEN"))

    # Quantization configuration
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype="float16",
        bnb_4bit_use_double_quant=True,
    )

    # Pipeline configuration
    pipeline_kwargs = dict(
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=0.8, # keep this high, otherwise model may lock to repeat "-" symbol
        repetition_penalty=1.1, # Avoid repetition
        return_full_text=False, 
    )

    try:
        # Load the model
        llm = HuggingFacePipeline.from_model_id(
            model_id=model_name,
            task="text-generation",
            device_map="auto",
            model_kwargs={"quantization_config": quantization_config} if quantization else {},
            pipeline_kwargs=pipeline_kwargs
        )

    except Exception as e:
        logger(f"Error loading model: {e}")
        return ResponseMessage(status_code=500, content="Error loading HuggingFace model")

    return llm


def json_parser(response: str) -> OptimizerResponse:
    """Parse the JSON response from the model"""
    
    try:

        # Use regex to extract JSON part (first occurrence of {...})
        json_match = re.search(r"\{.*?\}", response, re.DOTALL)

        json_str = json_match.group(0)  # Extract JSON string

        if os.getenv("DEBUG"):
            print(f"JSON String: {json_str}")

        # Parse and validate JSON using Pydantic
        parsed_json = json.loads(json_str)

        if os.getenv("DEBUG"):
            print(f"Type of parsed JSON: {type(parsed_json)}")
            print(f"Parsed JSON: {parsed_json}")

        return OptimizerResponse(content=parsed_json["output"], status=True)

    except Exception as e:
        logger.info(f"Error reconstructing JSON: {e}, Please try simplifying the request.")
        return OptimizerResponse(content=response, status=True)


def get_optimal_query(request: OptimizerRequest) -> OptimizerResponse:
    """Optimize the query for retrieval tasks"""

    # Set debug and verbose mode
    if os.getenv("DEBUG"):
        set_debug(True)
        set_verbose(True)

    # get model
    model = get_hf_model()

    # Define prompt
    prompt = PromptTemplate.from_template(template=OPTIMIZER_PROMPT)

    # Define the chain
    chain = prompt | model

    # Invoke the chain
    start_time = time.time()
    optimal_query = chain.invoke({"query": request.message})
    end_time = time.time() - start_time

    if os.getenv("DEBUG"):
        logger.info(f"Optimized Query: {optimal_query}")
        logger.info(f"Time taken to generate optimized query: {end_time}")

    # Parse the response
    parsed_response = json_parser(optimal_query)

    return parsed_response
