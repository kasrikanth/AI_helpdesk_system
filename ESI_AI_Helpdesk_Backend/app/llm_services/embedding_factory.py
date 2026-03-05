from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from app.llm_services.llm_config import (
    EMBEDDING_PROVIDER,
    OPENAI_API_KEY,
    OLLAMA_BASE_URL
)

def get_embedder():

    if EMBEDDING_PROVIDER == "openai":
        return OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=OPENAI_API_KEY
        )

    elif EMBEDDING_PROVIDER == "ollama":
        return OllamaEmbeddings(
            base_url=OLLAMA_BASE_URL,
            model="nomic-embed-text"
        )

    else:
        raise ValueError(f"Unsupported embedding provider: {EMBEDDING_PROVIDER}")