# version 3

import yaml
from pathlib import Path
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import delete
from app.models.database import KBDocument
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.utils.config import OPENAI_API_KEY
import logging


KB_DIR = "kbs"


def sanitize_metadata(metadata: dict) -> dict:
    clean = {}
    for k, v in metadata.items():
        if isinstance(v, (date, datetime)):
            clean[k] = v.isoformat()
        elif isinstance(v, (str, int, float, bool, list)) or v is None:
            clean[k] = v
        else:
            clean[k] = str(v)
    return clean


def parse_markdown(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---"):
        raise ValueError(f"{file_path.name} missing YAML front-matter")

    _, yaml_block, body = content.split("---", 2)
    metadata = yaml.safe_load(yaml_block)

    return metadata, body.strip()


def load_kbs(db: Session, created_by: str, replace_existing: bool = False):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80
    )

    embedder = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=OPENAI_API_KEY
    )

    for md_file in Path(KB_DIR).glob("*.md"):

        metadata, body = parse_markdown(md_file)
        kb_id = metadata.get("id")

        if not kb_id:
            raise ValueError(f"{md_file.name} missing 'id' in YAML")

        # 🔹 Delete old version if updating
        if replace_existing:
            db.execute(
                delete(KBDocument).where(
                    KBDocument.doc_metadata["kb_id"].astext == kb_id
                )
            )

        chunks = splitter.split_text(body)
        embeddings = embedder.embed_documents(chunks)

        for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):

            doc = KBDocument(
                title=metadata.get("title"),
                content=chunk,
                embedding=emb,
                chunk_index=str(i),
                original_doc_id=None,
                created_by=created_by,
                updated_by=created_by,
                doc_metadata=sanitize_metadata({
                    "kb_id": kb_id,
                    "title": metadata.get("title"),
                    "version": metadata.get("version"),
                    "tags": metadata.get("tags", []),
                    "last_updated": metadata.get("last_updated"),
                    "source_file": md_file.name
                })
            )

            db.add(doc)

    db.commit()
    print("Knowledge Base loaded and indexed")

