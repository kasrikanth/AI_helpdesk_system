from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.utils.config import get_db
from app.utils.dependencies import get_current_user
from app.models.database import Ticket
from app.apis.api_schema import (TicketResponse,TicketUpdate)

ticket_router = APIRouter()

def require_roles(allowed_roles: list, current_user):
    if current_user["role"] not in allowed_roles:
        raise HTTPException(403, "Permission denied")


@ticket_router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(404, "Ticket not found")
    
    if current_user["role"] in ["trainee", "operator"]:
        if ticket.user_role != current_user["role"]:
            raise HTTPException(403, "Not allowed")

    return ticket


@ticket_router.get("/", response_model=List[TicketResponse])
def get_all_tickets(
    status: str = None,
    tier: str = None,
    severity: str = None,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)):

    require_roles(
    ["support_engineer", "admin", "super_admin"],
    current_user)
    try:
        query = db.query(Ticket)
        
        if status:
            query = query.filter(Ticket.status == status)
        if tier:
            query = query.filter(Ticket.tier == tier)
        if severity:
            query = query.filter(Ticket.severity == severity)
        tickets = query.order_by(Ticket.created_at.desc()).limit(limit).all()
        
        return tickets
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to list tickets")



@ticket_router.patch("/update/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: str,
    req: TicketUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_roles(
    ["support_engineer", "admin", "super_admin"],
    current_user
)
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(404, "Ticket not found")

    if req.status:
        ticket.status = req.status

    if req.tier:
        ticket.tier = req.tier.value

    if req.severity:
        ticket.severity = req.severity.value

    db.commit()
    db.refresh(ticket)

    return ticket
