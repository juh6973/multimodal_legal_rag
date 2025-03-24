import os
import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from models.query_models import RagResponse, Document
from utils.logger_config import logger


def get_client() -> Chroma:
    """Get the client for the ChromaDB API"""
    try:
        embedding_function = HuggingFaceEmbeddings(model_name="intfloat/e5-large-v2")

        chroma_client = Chroma(
            collection_name=os.getenv("CHROMA_COLLECTION"),
            client=chromadb.HttpClient(host=os.getenv("CHROMA_HOST")),
            embedding_function=embedding_function,
        )
    except Exception as e:
        logger.error(f"Error loading Chroma client: {e}")
        raise e

    return chroma_client


def query_rag(query:str) -> RagResponse:
    """Query the RAG model with the given query"""
    # Get the client
    client = get_client()

    try:
        # Get the response
        results = client.similarity_search_with_relevance_scores(query, k=5, score_threshold=0.7)

        documents = [Document(content=res[0].page_content, id=res[0].id, meta_data=res[0].metadata) for res in results]
        scores = [res[1] for res in results]

        return RagResponse(content=documents, score=scores)
    except Exception as e:
        logger.error(f"Error querying RAG model: {e}")
        raise e


        

