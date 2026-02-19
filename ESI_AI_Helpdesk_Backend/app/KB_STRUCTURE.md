# Knowledge Base (KB) Structure

## Overview
The Knowledge Base (KB) is a critical component of the ESI AI Helpdesk Backend. It stores and organizes information to assist in resolving user queries and generating intelligent responses. The KB is designed to be easily ingested, indexed, and retrieved for efficient operations.

## Storage
- **File System**:
  - The KB articles are stored as Markdown files in the `kbs/` directory.
  - Each file represents a specific topic or document, named systematically for easy identification (e.g., `01-access-and-authentication-v2.1.md`).
- **Database**:
  - Metadata about the KB articles, such as titles, tags, and creation dates, is stored in a SQLite database (`chroma.sqlite3`).

## Ingestion
1. **Process**:
   - The ingestion process reads Markdown files from the `kbs/` directory.
   - Each file is parsed to extract its content, metadata, and structure.
2. **Tools**:
   - The `kb_loader.py` script handles the ingestion process.
   - It ensures that the content is cleaned, tokenized, and stored in the database for indexing.
3. **Metadata Extraction**:
   - Titles, tags, and other metadata are extracted from the file headers or predefined sections.

## Indexing
1. **Vectorization**:
   - The content of each KB article is converted into vector embeddings using a pre-trained language model.
   - These embeddings capture the semantic meaning of the text.
2. **Storage**:
   - The embeddings are stored in the `chroma.sqlite3` database for efficient similarity searches.
3. **Indexing Tool**:
   - The `retriever.py` module is responsible for indexing and managing the embeddings.

## Retrieval
- **Similarity Search**:
  - When a user submits a query, the `retriever.py` module performs a similarity search against the indexed embeddings.
  - The most relevant KB articles are retrieved based on their semantic similarity to the query.
- **Integration with LLM**:
  - The retrieved articles are passed to the `llm.py` module for generating context-aware responses.

## Benefits
- **Scalability**:
  - The modular design allows for easy addition of new KB articles.
- **Efficiency**:
  - Vector-based indexing ensures fast and accurate retrieval.
- **Flexibility**:
  - Supports various formats and topics, making it adaptable to different domains.