# Metrics.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.apis.api_schema import MetricsSummary, MetricsTrends, TrendDataPoint
from app.models.database import Conversation, Message, Ticket, GuardrailEvent
from app.utils.config import get_db


metrics_router = APIRouter()

@metrics_router.get("/summary", response_model=MetricsSummary)
def fetch_metrics_overview(db: Session = Depends(get_db)):
    try:
        # Core counts
        conversation_count = db.query(func.count(Conversation.id)).scalar() or 0
        ticket_count = db.query(func.count(Ticket.id)).scalar() or 0
        guardrail_count = db.query(func.count(GuardrailEvent.id)).scalar() or 0

        # Deflection Rate
        resolved_without_ticket = max(conversation_count - ticket_count, 0)
        deflection_percentage = (
            (resolved_without_ticket / conversation_count) * 100
            if conversation_count > 0 else 0.0
        )

        # Average Assistant Confidence
        avg_conf = (
            db.query(func.avg(Message.confidence))
            .filter(
                Message.role == "assistant",
                Message.confidence.isnot(None)
            )
            .scalar()
        )
        avg_confidence_value = float(avg_conf) if avg_conf else 0.0

        # Tickets grouped by tier
        tier_distribution = dict(
            db.query(Ticket.tier, func.count(Ticket.id))
            .group_by(Ticket.tier)
            .all()
        )

        # Tickets grouped by severity
        severity_distribution = dict(
            db.query(Ticket.severity, func.count(Ticket.id))
            .group_by(Ticket.severity)
            .all()
        )

        # Escalations (example: Tier 3 tickets treated as escalation)
        escalation_total = db.query(func.count(Ticket.id)).filter(
            Ticket.tier == "tier_3"
        ).scalar() or 0

        # Most common issue categories (assuming Ticket.category exists)
        category_distribution = dict(
            db.query(Ticket.tier, func.count(Ticket.id))
            .group_by(Ticket.tier)
            .order_by(func.count(Ticket.id).desc())
            .all()
        )

        return MetricsSummary(
            total_conversations=conversation_count,
            total_tickets=ticket_count,
            deflection_rate=round(deflection_percentage, 2),
            avg_confidence=round(avg_confidence_value, 2),
            guardrail_activations=guardrail_count,
            tickets_by_tier=tier_distribution,
            tickets_by_severity=severity_distribution,
            escalation_count=escalation_total,
            top_issue_categories=category_distribution
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to compute metrics summary."
        )


@metrics_router.get("/trends", response_model=MetricsTrends)
def fetch_metrics_trends(db: Session = Depends(get_db)):
    try:
        # Daily Conversation Volume
        conversation_trend = db.query(
            func.date(Conversation.created_at),
            func.count(Conversation.id)
        ).group_by(
            func.date(Conversation.created_at)
        ).order_by(
            func.date(Conversation.created_at)
        ).all()

        conversation_points = [
            TrendDataPoint(date=str(day), value=count)
            for day, count in conversation_trend
        ]

        # Guardrail Activation Trend
        guardrail_trend = db.query(
            func.date(GuardrailEvent.created_at),
            func.count(GuardrailEvent.id)
        ).group_by(
            func.date(GuardrailEvent.created_at)
        ).order_by(
            func.date(GuardrailEvent.created_at)
        ).all()

        guardrail_points = [
            TrendDataPoint(date=str(day), value=count)
            for day, count in guardrail_trend
        ]

        # Ticket Volume Trend
        ticket_trend = db.query(
            func.date(Ticket.created_at),
            func.count(Ticket.id)
        ).group_by(
            func.date(Ticket.created_at)
        ).order_by(
            func.date(Ticket.created_at)
        ).all()

        ticket_points = [
            TrendDataPoint(date=str(day), value=count)
            for day, count in ticket_trend
        ]

        return MetricsTrends(
            conversation_volume=conversation_points,
            guardrail_activations=guardrail_points,
            ticket_volume=ticket_points
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to generate trend metrics."
        )
