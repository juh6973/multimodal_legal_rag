import json
import os
import re
import time

from pydantic import ValidationError
from langchain_huggingface import  HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.globals import set_verbose, set_debug

from transformers import BitsAndBytesConfig
from huggingface_hub.commands.user import login

from models.query_models import OptimizerRequest, OptimizerResponse


def get_hf_model(model_name: str = "mistralai/Mistral-7B-Instruct-v0.3") -> HuggingFacePipeline: 
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
        max_new_tokens=2048,  # Increase this value
        do_sample=True,  # Enable sampling
        #temperature=0.8, # keep this high
        repetition_penalty=1.03,
        return_full_text=False, # Return answer only
    )
    try:
        # Load the model
        llm = HuggingFacePipeline.from_model_id(
            model_id=model_name,
            task="text-generation",
            device_map="auto",
            model_kwargs={"quantization_config": quantization_config},
            pipeline_kwargs=pipeline_kwargs
        )
    except Exception as e:
        print(f"Error loading model: {e}")
        raise e

    return llm


def json_parser(response: str) -> OptimizerResponse:
    """Parse the JSON response from the model"""
    
    try:
        if os.getenv("DEBUG"):
            print(f"Response: {response}")
        # Use regex to extract JSON part (first occurrence of {...})
        json_match = re.search(r"\{.*?\}", response, re.DOTALL)
        if not json_match:
            raise ValueError("No valid JSON found in response.")

        json_str = json_match.group(0)  # Extract JSON string
        if os.getenv("DEBUG"):
            print(f"JSON String: {json_str}")
        # Parse and validate JSON using Pydantic
        parsed_json = json.loads(json_str)
        if os.getenv("DEBUG"):
            print(f"Type of parsed JSON: {type(parsed_json)}")
            print(f"Parsed JSON: {parsed_json}")

        return OptimizerResponse(content=parsed_json["output"], status=True)

    except (json.JSONDecodeError, ValidationError) as e:
        print(f"Error reconstructing JSON: {e}, Please try simplifying the request.")
        return OptimizerResponse(content=response, status=False, error=str(e))


def get_optimal_query(request: OptimizerRequest) -> OptimizerResponse:
    """Optimize the query for retrieval tasks"""

    # Set debug and verbose mode
    if os.getenv("DEBUG"):
        set_debug(True)
        set_verbose(True)

    # get model
    model = get_hf_model()

    # Define prompt
    prompt_template = """
        You are a legal NLP assistant. Your task is to analyze a detailed legal situation and generate a concise, optimized query for a retrieval system.

        **Instructions:**
        1. Identify the core legal issue(s).
        2. Use precise legal terminology.
        3. Keep the output **concise (max 20 words)** for retrieval.
        4. Format JSON response as following {{"output": }}

        Here is an example of a user scenario and an optimized query:
        **User Scenario:** 
        I was working at a company for five years, and recently, they fired me without any warning. 
        I never received any performance warnings or complaints. I believe this was an unfair dismissal. 
        What legal actions can I take against my employer?

        **Answer:**
        {{"output": "Legal remedies for wrongful termination without notice under labor laws and case law precedents."}}
        
        Now, generate an optimized query for the following scenario:
        **User Scenario:**
        {query}
        
        **Answer:**
        {{"output": }}
        """
    
    prompt = PromptTemplate.from_template(template=prompt_template)

    # Define the chain
    chain = prompt | model

    # Invoke the chain
    start_time = time.time()
    optimal_query = chain.invoke({"query": request.message})
    print("Time taken: ", time.time() - start_time)

    parsed_response = json_parser(optimal_query)

    return parsed_response



def main():
    #msg = "A small business owner signs a contract with a supplier to deliver goods by a specific date. The supplier fails to deliver the goods on time, causing significant financial losses to the business owner. The contract does not explicitly specify damages for late delivery. Considering contract law principles, what legal remedies could the business owner seek, and how would a court likely assess the claim for damages in this scenario?"
    msg = "I recently discovered that another company is using my copyrighted images without permission on their website. I own full rights to these images, and they are benefiting commercially from them. What legal actions can I take?"
    query = OptimizerRequest(message=msg)
    get_optimal_query(query)


if __name__ == "__main__":
    main()