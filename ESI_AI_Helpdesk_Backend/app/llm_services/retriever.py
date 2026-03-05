# retriever.py

from sqlalchemy import text
from app.utils.config import SessionLocal, OPENAI_API_KEY
# from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from app.llm_services.embedding_factory import get_embedder

# embedder = OpenAIEmbeddings(
#     model="text-embedding-3-small",
#     openai_api_key=OPENAI_API_KEY
# )

embedder = get_embedder()

# Minimum similarity threshold — documents below this are too weak to use
MIN_SIMILARITY_THRESHOLD = 0.20

def retrieve_kb(question: str, k: int = 5):
    db = SessionLocal()
    query_embedding = embedder.embed_query(question)

    sql = text("""
        SELECT id, title, content, doc_metadata,
               1 - (embedding <=> CAST(:embedding AS vector)) AS score
        FROM kb_documents
        ORDER BY embedding <=> CAST(:embedding AS vector)
        LIMIT :k
    """)

    results = db.execute(sql, {
        "embedding": query_embedding,
        "k": k
    }).fetchall()

    db.close()

    documents = []

    for row in results:
        similarity = float(row.score)

        # Skip documents that are too weakly related
        if similarity < MIN_SIMILARITY_THRESHOLD:
            continue
        documents.append({
            "doc": Document(
                page_content=row.content,
                metadata=row.doc_metadata or {}
            ),
            "score": similarity,
            "similarity": similarity  # FIX: was missing — confidence calculator reads this key
        })

    return documents


