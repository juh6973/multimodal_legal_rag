import os
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from utils.prompts import SYSTEM_MESSAGE
from models.query_models import OptimizerRequest
from services.query_optimizer import get_hf_model, get_optimal_query
from services.rag import get_knowledge, query_rag, store_knowledge
from services.formatter_model import format_context

from utils.logger_config import logger


def is_question(input_text: str) -> bool:
    """Check if the input is a question"""
    question_words = {"what", "who", "where", "when", "why", "how", "is", "does", "can", "should"}
    return input_text.strip().endswith("?") or input_text.lower().split()[0] in question_words


def format_history(messages: list):
    """Format the chat history"""

    history = []

    # Add the messages to the history
    for msg in messages:
        if msg["role"] == "user":
            history.append(HumanMessage(msg["content"]))
        if msg["role"] == "assistant":
            history.append(AIMessage(msg["content"]))
    return history


def chat_model(prompt:str, messages: list):
    """Chat with the model"""
    # Format the chat history
    history = format_history(messages=messages)

    # Check if the input is a question, update knowledge if it is
    if is_question(input_text=prompt):
        optimized_query = get_optimal_query(OptimizerRequest(message=prompt))
        rag_response = query_rag(query=optimized_query.content)
        store_knowledge(documents=rag_response)

    # Get documents from ChromaDB memory
    memory = get_knowledge()
    context = format_context(documents=memory)

    if os.getenv("DEBUG"):
        logger.info(f"Chat History: {history}")
        logger.info(f"Prompt: {prompt}")
        logger.info(f"Legal Context: {context}")

    # Get the model
    llm = get_hf_model()

    # Get the prompt
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_MESSAGE),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    # Define chain
    chain = prompt_template | llm

    # Run the pipeline
    response = chain.invoke(
        {
            "chat_history": history,
            "input": prompt,
            "legal_context": context,
        }
    )

    return response

    