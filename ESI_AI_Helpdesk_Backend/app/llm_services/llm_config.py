import os

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "openai")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")