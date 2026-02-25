# chat.py
# version 3

import logging
from aiohttp import request
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import delete
from sqlalchemy.orm import Session
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from app.kb_loader import load_kbs, parse_markdown, sanitize_metadata
from app.apis.api_schema import ChatRequest, ChatResponse, KBReference
from app.apis.api_schema import KBCreateRequest, KBUpdateRequest
from app.utils.dependencies import get_current_user
from app.utils.config import get_db
from app.utils.config import OPENAI_API_KEY
from app.models.database import KBDocument, Message, UserSession, Conversation, Ticket, GuardrailEvent
from app.llm_services.retriever import retrieve_kb
from app.llm_services.llm import generate_answer, compute_response_confidence
from app.llm_services.escalate_classifier import classify_tier, classify_severity, should_escalate
from app.utils.Guardrail import check_guardrail
from app.models.database import User
from uuid import uuid4
from pathlib import Path
import json

router = APIRouter()

# Chat Endpoint for user to ask question

@router.post("/chat", response_model=ChatResponse)
def chat(
    req: ChatRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:

        # Validate Active Session
        session = db.query(UserSession).filter(UserSession.id == req.sessionId,
        UserSession.user_id == current_user["sub"],
        UserSession.is_active == True).first()

        if not session:
            raise HTTPException(401, "No active session")

        # Get or create conversation
        conversation = db.query(Conversation).filter(
            Conversation.session_id == session.id).first()

        if not conversation:
            conversation = Conversation(session_id=session.id,
                user_role=current_user["role"])
            db.add(conversation)
            db.commit()
            db.refresh(conversation)

        # Fetch User Role from DB
        user = db.query(User).filter(User.id == current_user["sub"]).first()
        user_role = user.role.name
        print(f"User {user.email} with role {user_role} (level {user.role.level}) is making a request.")

        prior_assistant_messages = db.query(Message).filter(
            Message.conversation_id == conversation.id,
            Message.role == "assistant"
        ).count()

        # Also check explicit user language signaling repeated failure
        REPEATED_FAILURE_SIGNALS = [
            "tried", "already", "still not", "didn't work", "doesn't work",
            "still stuck", "same issue", "again", "twice", "multiple times",
            "still broken", "still failing", "persists", "keeps happening"
        ]
        user_signals_repeat = any(
            signal in req.message.lower()
            for signal in REPEATED_FAILURE_SIGNALS
        )

        # Escalate if either: 2+ prior replies OR user explicitly says it's a repeat
        repeated_failure = (prior_assistant_messages >= 2) or user_signals_repeat

        #================== GUARDRAIL CHECK =================
        guardrail = check_guardrail(req.message)

        if guardrail.blocked:
            # Store guardrail violation message
            user_message = Message(conversation_id=conversation.id,
            role="user",content=req.message
            )
            db.add(user_message)
            db.commit()

            guardrail_event = GuardrailEvent(
                id = str(uuid4()),
                conversation_id=conversation.id,
                message_id=user_message.id,
                severity=guardrail.severity,
                user_message=req.message)
            db.add(guardrail_event)
            db.commit()

            assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            confidence=0.0,
            content=f"Guardrail triggered: {guardrail.reason}"
            )
            db.add(assistant_message)
            db.commit()
                        
            return ChatResponse(
                answer="I'm sorry, the question you asked violates our usage policies and cannot be processed.",
                kbReferences=[],     
                confidence=0.0,
                tier="TIER_3",
                severity=guardrail.severity,
                needsEscalation=True,
                guardrail=guardrail,
                ticket_id=None
            )
        
        # Store user message without guardrail violation
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=req.message
        )
        db.add(user_message)
        db.commit()

        # Retrieve KB
        documents = retrieve_kb(req.message)
        kb_coverage = len(documents) > 0

        if not kb_coverage:
            out_of_scope_reply = (
                "I'm sorry, I can only answer questions related to the CyberLab "
                "Training Platform — such as authentication, virtual labs, containers, "
                "DNS, and access issues.If you believe this is a platform-related "
                "issue, please try rephrasing your question."
            )
            assistant_message = Message(
                conversation_id=conversation.id,
                role="assistant",
                confidence=0.0,
                content=out_of_scope_reply
            )
            db.add(assistant_message)
            db.commit()

            return ChatResponse(
                answer=out_of_scope_reply,
                kbReferences=[],
                confidence=0.0,
                tier="TIER_0",
                severity="LOW",
                needsEscalation=False,
                guardrail=guardrail,
                ticket_id=None,
                ticket_status=None)

        docs = [r["doc"] for r in documents]

        # Generate Answer
        answer = generate_answer(req.message, docs, user_role=user_role)

        # Calculate Confidence
        confidence = compute_response_confidence(
            docs=[{"similarity": r.get("similarity", r.get("score", 0.0))} 
                for r in documents],
            response_text=answer
        )

        # Severity check
        severity = classify_severity(req.message)

        # Tier check
        tier = classify_tier(req.message,severity,kb_coverage,repeated_failure=repeated_failure)

        #============ Escalation handler =================#
        needs_escalation = should_escalate(tier,severity,
             kb_coverage,repeated_failure=repeated_failure)

        ticket = None

        last_ticket = db.query(Ticket).order_by(Ticket.created_at.desc()).first()
        if last_ticket and last_ticket.id.startswith("TICK-"):
            last_number = int(last_ticket.id.split("-")[1])
            new_number = last_number + 1
        else:
            new_number = 1

        new_ticket_id = f"TICK-{new_number:05d}"

        # Escalation Ticket Creation
        if needs_escalation:
            ticket = Ticket(
                id=new_ticket_id,
                conversation_id=conversation.id,
                user_id = current_user["sub"],
                subject=req.message[:200],
                description=req.message,
                tier=tier.value,
                severity=severity.value,
                status="OPEN",
                user_role=user_role,
                context=req.context.dict() if req.context else {},
                created_by = user.full_name,
                updated_by = user.full_name
            )
            db.add(ticket)
            db.commit()

            assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            confidence = confidence,
            content=f"Escalated ticket created: {ticket.id}"
            )
            db.add(assistant_message)
            db.commit()

            return ChatResponse(
            answer=answer,
            kbReferences=[
                KBReference(
                    id=r["doc"].metadata.get("kb_id"),
                    title=r["doc"].metadata.get("title", "KB Article")
                )
                for r in documents
            ],
            confidence=confidence,
            tier=tier,
            severity=severity,
            needsEscalation=needs_escalation,
            guardrail=guardrail,
            ticket_id=ticket.id,
            ticket_status=(
                    f"A support ticket ({ticket.id}) has been created and assigned to "
                    f"{tier.value}. Our team will follow up with you shortly."
                )
            )

        # Store assistant message
        assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            confidence = confidence,
            content=answer
        )
        db.add(assistant_message)
        db.commit()

        return ChatResponse(
            answer=answer,
            kbReferences=[
                KBReference(
                    id=r["doc"].metadata.get("kb_id"),
                    title=r["doc"].metadata.get("title", "KB Article")
                )
                for r in documents
            ],
            confidence=confidence,
            tier=tier,
            severity=severity,
            needsEscalation=needs_escalation,
            guardrail=guardrail
        )

    except Exception as e:
        logging.error(f"Chat error: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")


# KB Create Endpoint KBs documents are updated by user
@router.post("/kb/create")
def create_kb(
    req: KBCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    
    try:
        logging.info("Starting KB ingestion...")

        # 🔹 Fetch user from DB using payload
        user = db.query(User).filter(User.id == current_user.get("sub")).first()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        load_kbs(db=db,
            # created_by=current_user.username,
            created_by=user.full_name,
            replace_existing=req.replace_existing)

        return {
            "message": "Knowledge Base stored successfully",
            "replace_existing": req.replace_existing
        }

    except Exception as e:
        db.rollback()
        logging.error(f"KB ingestion failed: {str(e)}")
        raise HTTPException(status_code=500, detail="KB ingestion failed")

# KB Update Endpoint KBs documents are updated by user
@router.put("/kb/update")
def update_kb(
    req: KBUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    KB_DIR = "kbs"
    try:
        md_file = Path(KB_DIR) / f"{req.kb_id}.md"

        if not md_file.exists():
            raise HTTPException(status_code=404, detail="KB file not found")

        metadata, body = parse_markdown(md_file)

        user = db.query(User).filter(User.id == current_user.get("sub")).first()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        # 🔹 Delete old chunks
        db.execute(
            delete(KBDocument).where(
                KBDocument.doc_metadata["kb_id"].astext == req.kb_id
            )
        )

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=80
        )

        embedder = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=OPENAI_API_KEY
        )

        chunks = splitter.split_text(body)
        embeddings = embedder.embed_documents(chunks)

        for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
            doc = KBDocument(
                title=metadata.get("title"),
                content=chunk,
                embedding=emb,
                chunk_index=str(i),
                created_by=user.full_name,
                updated_by=user.full_name,
                doc_metadata=sanitize_metadata(metadata)
            )
            db.add(doc)

        db.commit()

        return {"message": f"KB '{req.kb_id}' updated successfully"}

    except Exception as e:
        db.rollback()
        logging.error(f"KB update failed: {str(e)}")
        raise HTTPException(status_code=500, detail="KB update failed")


