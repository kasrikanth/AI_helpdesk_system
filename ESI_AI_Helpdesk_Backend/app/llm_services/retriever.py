# retriever.py

from sqlalchemy import text
from app.utils.config import SessionLocal, OPENAI_API_KEY
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document


embedder = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=OPENAI_API_KEY
)

def retrieve_kb(question: str, k: int = 1):
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
        documents.append({
            "doc": Document(
                page_content=row.content,
                metadata=row.doc_metadata or {}
            ),
            "score": float(row.score)  # IMPORTANT
        })

    return documents


