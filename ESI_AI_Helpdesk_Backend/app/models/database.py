# we going to use local system postgresql and pgvector for kbs embedding storage and retrieval.

from sqlalchemy import (Column, Integer, String, Text, Float, Boolean, ForeignKey, Index, func,)
from sqlalchemy.dialects.postgresql import UUID, JSONB, TIMESTAMP
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.utils.config import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),server_default=func.now(),onupdate=func.now())
    created_by = Column(String(255), nullable=True)

    role = relationship("Role", back_populates="users")
    sessions = relationship("UserSession",back_populates="user",cascade="all, delete-orphan")
    tickets = relationship("Ticket", back_populates="user", cascade="all, delete-orphan")
    

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    level = Column(Integer, nullable=False)  # privilege hierarchy

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),server_default=func.now(),onupdate=func.now())
    created_by = Column(String(255), nullable=True)
    updated_by = Column(String(255), nullable=True)

    # relationships
    users = relationship("User", back_populates="role")

class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, index=True)
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=True)
    ip_address = Column(String(50))
    user_agent = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    expires_at = Column(TIMESTAMP(timezone=True), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    conversations = relationship("Conversation",back_populates="session",
                                 cascade="all, delete-orphan")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("user_sessions.id", ondelete="CASCADE"),nullable=False, index=True)
    user_role = Column(String(50), nullable=False)
    context = Column(JSONB, server_default="{}")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(),nullable=False)

    # Relationships
    session = relationship("UserSession", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation",cascade="all, delete-orphan")
    tickets = relationship("Ticket", back_populates="conversation")
    guardrail_events = relationship("GuardrailEvent",back_populates="conversation",cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"),nullable=False,
        index=True)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    kb_references = Column(JSONB, server_default="[]")
    confidence = Column(Float, nullable=True)
    tier = Column(String(20), nullable=True)
    severity = Column(String(20), nullable=True)
    guardrail_blocked = Column(Boolean, server_default="false")
    created_at = Column(TIMESTAMP(timezone=True),server_default=func.now(),nullable=False)

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    guardrail_events = relationship("GuardrailEvent", back_populates="message")

class KBDocument(Base):
    __tablename__ = "kb_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(1536), nullable=False)
    doc_metadata = Column(JSONB, server_default="{}")
    chunk_index = Column(String(10), nullable=True)
    original_doc_id = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),server_default=func.now(),nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),server_default=func.now(),onupdate=func.now())
    created_by = Column(String(255), nullable=True)
    updated_by = Column(String(255), nullable=True)


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(String(50), primary_key=True)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"),
                             nullable=False,index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    subject = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    tier = Column(String(20), nullable=False)
    severity = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False, server_default="OPEN")
    user_role = Column(String(50), nullable=False)
    context = Column(JSONB, server_default="{}")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(),nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)
    created_by = Column(String(255), nullable=False)
    updated_by = Column(String(255), nullable=False)

    # Relationships
    conversation = relationship("Conversation", back_populates="tickets")
    user = relationship("User", back_populates="tickets")


class GuardrailEvent(Base):
    __tablename__ = "guardrail_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"),nullable=False,index=True)
    message_id = Column(UUID(as_uuid=True),ForeignKey("messages.id", ondelete="SET NULL"),nullable=True)
    severity = Column(String(20), nullable=False)
    user_message = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),server_default=func.now(),nullable=False)

    
    #relationships
    conversation = relationship("Conversation", back_populates="guardrail_events")
    message = relationship("Message", back_populates="guardrail_events")