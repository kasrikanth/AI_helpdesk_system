# app/apis/metrics.py

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct

from app.apis.api_schema import MetricsSummary, MetricsTrends, TrendDataPoint
from app.models.database import Conversation, Message, Ticket, GuardrailEvent
from app.utils.config import get_db

metrics_router = APIRouter()

@metrics_router.get("/summary", response_model=MetricsSummary)
def fetch_metrics_overview(db: Session = Depends(get_db)):
    try:
        conversation_count = db.query(func.count(Conversation.id)).scalar() or 0

        ticket_count = db.query(func.count(Ticket.id)).scalar() or 0

        guardrail_count = db.query(func.count(GuardrailEvent.id)).scalar() or 0

        conversations_with_ticket = (
            db.query(func.count(distinct(Ticket.conversation_id)))
            .filter(Ticket.conversation_id.isnot(None))
            .scalar()
            or 0
        )

        # conversation resolved without tickets
        resolved_without_ticket = max(
            conversation_count - conversations_with_ticket, 0
        )

        if conversation_count > 0:
            deflection_percentage = (
                resolved_without_ticket / conversation_count
            ) * 100
        else:
            deflection_percentage = 0.0

        avg_conf = (
            db.query(func.avg(Message.confidence))
            .filter(
                Message.role == "assistant",
                Message.confidence.isnot(None)
            )
            .scalar()
        )

        avg_confidence_value = float(avg_conf) if avg_conf else 0.0

   
        tier_distribution = dict(
            db.query(Ticket.tier, func.count(Ticket.id))
            .group_by(Ticket.tier)
            .all()
        )

        severity_distribution = dict(
            db.query(Ticket.severity, func.count(Ticket.id))
            .group_by(Ticket.severity)
            .all()
        )


        return MetricsSummary(
            total_conversations=conversation_count,
            total_tickets=ticket_count,
            deflection_rate=round(deflection_percentage, 2),
            avg_confidence=round(avg_confidence_value, 2),
            guardrail_activations=guardrail_count,
            tickets_by_tier=tier_distribution,
            tickets_by_severity=severity_distribution
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to compute metrics summary: {str(e)}"
        )



@metrics_router.get("/trends", response_model=MetricsTrends)
def fetch_metrics_trends(db: Session = Depends(get_db)):
    try:

        conversation_trend = (
            db.query(
                func.date_trunc("day", Conversation.created_at).label("day"),
                func.count(Conversation.id)
            )
            .group_by("day")
            .order_by("day")
            .all()
        )

        conversation_points = [
            TrendDataPoint(
                start_date=day,
                end_date=day + timedelta(days=1),
                value=count
            )
            for day, count in conversation_trend
        ]

        guardrail_trend = (
            db.query(
                func.date_trunc("day", GuardrailEvent.created_at).label("day"),
                func.count(GuardrailEvent.id)
            )
            .group_by("day")
            .order_by("day")
            .all()
        )

        guardrail_points = [
            TrendDataPoint(
                start_date=day,
                end_date=day + timedelta(days=1),
                value=count
            )
            for day, count in guardrail_trend
        ]


        ticket_trend = (
            db.query(
                func.date_trunc("day", Ticket.created_at).label("day"),
                func.count(Ticket.id)
            )
            .group_by("day")
            .order_by("day")
            .all()
        )

        ticket_points = [
            TrendDataPoint(
                start_date=day,
                end_date=day + timedelta(days=1),
                value=count
            )
            for day, count in ticket_trend
        ]
        return MetricsTrends(
            conversation_volume=conversation_points,
            guardrail_activations=guardrail_points,
            ticket_volume=ticket_points
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to compute metrics trends: {str(e)}"
        )