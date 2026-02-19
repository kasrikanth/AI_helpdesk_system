# api_schema.py

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from app.apis.pydantic_models import (TierLevel,SeverityLevel)

# -----------------------
# AUTH SCHEMAS
# -----------------------

class LoginRequest(BaseModel):
    email: str
    password: str


class CreateUserRequest(BaseModel):
    email: str
    password: str
    full_name: str
    role_name: str

# -----------------------
# CHAT SCHEMAS
# -----------------------

class ChatContext(BaseModel):
    module: Optional[str] = "default-module"
    channel: Optional[str] = "self-service-portal"


class ChatRequest(BaseModel):
    sessionId: str
    message: str = Field(..., min_length=1)
    context: Optional[ChatContext] = None


class KBReference(BaseModel):
    id: str
    title: str


class GuardrailStatus(BaseModel):
    blocked: bool
    reason: Optional[str] = None
    severity: Optional[str] = None



class ChatResponse(BaseModel):
    answer: str
    kbReferences: List[KBReference]
    confidence: float = Field(..., ge=0.0, le=1.0)
    tier: TierLevel
    severity: SeverityLevel
    needsEscalation: bool
    guardrail: GuardrailStatus
    ticket_id: Optional[str] = None
    ticket_status: Optional[str] = None


# -----------------------
# TICKET SCHEMAS
# -----------------------

# class TicketCreate(BaseModel):
#     subject: str
#     description: str
#     tier: TierLevel
#     severity: SeverityLevel
#     context: Optional[dict] = {}
#     ai_analysis: Optional[dict] = {}

class TicketCreate(BaseModel):
    sessionId: str
    subject: str
    description: str
    tier: TierLevel
    severity: SeverityLevel
    context: Optional[dict] = {}
    ai_analysis: Optional[dict] = {}

class TicketResponse(BaseModel):
    id: str
    conversation_id: UUID
    subject: str
    description: str
    tier: TierLevel
    severity: SeverityLevel
    status: str
    user_role: str
    context: dict
    ai_analysis: dict
    created_at: datetime
    updated_at: datetime
    model_config = {
        "from_attributes": True   #from_attributes = True (Pydantic v2)
    }

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    tier: Optional[TierLevel] = None
    severity: Optional[SeverityLevel] = None


# KB PYDANTIC SCHEMAS

# -------- Create KB --------
class KBCreateRequest(BaseModel):
    replace_existing: bool = False


# -------- Update KB -------
class KBUpdateRequest(BaseModel):
    kb_id: str



# Metrics API Schemas
class MetricsSummary(BaseModel):
    """Summary metrics response."""
    total_conversations: int
    total_tickets: int
    deflection_rate: float
    avg_confidence: float
    guardrail_activations: int
    tickets_by_tier: Dict[str, int]
    tickets_by_severity: Dict[str, int]


class TrendDataPoint(BaseModel):
    """Single data point in trend data."""
    timestamp: datetime
    value: float


class MetricsTrends(BaseModel):
    """Trend metrics response."""
    conversation_volume: List[TrendDataPoint]
    ticket_volume: List[TrendDataPoint]
    deflection_rate: List[TrendDataPoint]
    avg_confidence: List[TrendDataPoint]




# -------- Response --------
class KBIngestionResponse(BaseModel):
    message: str
    kb_id: Optional[str] = None
    total_chunks: Optional[int] = None
    version: Optional[str] = None

# -------- Metadata --------
class KBMetadata(BaseModel):
    kb_id: str
    title: str
    version: str
    tags: Optional[List[str]] = []
    last_updated: Optional[datetime] = None
    source_file: Optional[str] = None

# -------- Document Fetch --------
class KBDocumentResponse(BaseModel):
    id: UUID
    title: str
    content: str
    chunk_index: Optional[str]
    doc_metadata: KBMetadata

    class Config:
        from_attributes = True
