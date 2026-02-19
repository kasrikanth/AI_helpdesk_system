import logging
from fastapi import FastAPI
from app.apis.chat import router
from app.apis.auth import auth_router
from app.apis.tickets import ticket_router
from app.apis.metrics import metrics_router

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="ESI AI Help Desk")

# Include API routes
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(router, prefix="/api", tags=["chat"] )
app.include_router(ticket_router, prefix="/tickets", tags=["Tickets"])
app.include_router(metrics_router, prefix="/metrics", tags=["Metrics"])


