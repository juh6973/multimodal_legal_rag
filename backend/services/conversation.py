import os
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from utils.prompts import SYSTEM_MESSAGE
from services.query_optimizer import get_hf_model
from langchain_huggingface import HuggingFacePipeline


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


def chat_model(prompt:str, messages: list, context: str):
    """Chat with the model"""
    # Format the chat history
    history = format_history(messages=messages)

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

    