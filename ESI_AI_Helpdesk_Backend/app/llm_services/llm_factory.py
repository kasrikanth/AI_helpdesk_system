from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_community.chat_models import ChatOllama
from app.llm_services.llm_config import (
    LLM_PROVIDER,
    OPENAI_API_KEY,
    ANTHROPIC_API_KEY,
    OLLAMA_BASE_URL
)

def get_llm():

    if LLM_PROVIDER == "openai":
        return ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            temperature=0
        )

    elif LLM_PROVIDER == "anthropic":
        return ChatAnthropic(
            anthropic_api_key=ANTHROPIC_API_KEY,
            model="claude-3-sonnet-20240229",
            temperature=0
        )

    elif LLM_PROVIDER == "ollama":
        return ChatOllama(
            base_url=OLLAMA_BASE_URL,
            model="llama3",
            temperature=0
        )

    else:
        raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")