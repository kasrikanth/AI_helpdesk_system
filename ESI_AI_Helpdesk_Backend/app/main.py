import logging
from fastapi import FastAPI
from app.apis.chat import router
from app.apis.auth import auth_router
from app.apis.tickets import ticket_router
from app.apis.metrics import metrics_router
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="ESI AI Help Desk")

# CORS CONFIGURATION
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://ai-helpdesk-system.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(router, prefix="/api", tags=["chat"] )
app.include_router(ticket_router, prefix="/tickets", tags=["Tickets"])
app.include_router(metrics_router, prefix="/metrics", tags=["Metrics"])


# Health Check API
@app.get("/health", tags=["Health"])
async def health_check():
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "ESI AI Help Desk",
            "timestamp": datetime.now().strftime("%d-%m-%Y %I:%M:%S %p"),
            "version": "1.0.0"
        }
    )
