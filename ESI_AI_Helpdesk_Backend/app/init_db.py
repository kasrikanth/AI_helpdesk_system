# init_db.py

from app.utils.config import Base, engine
from app.models.database import (Conversation, Message, KBDocument, Ticket, 
GuardrailEvent, User, Role, UserSession)

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    create_tables()

# this is the command to initialize the database tables
# python -m app.init_db

#path
# (venv) PS D:\From FEB 2026\AI Full stack Challenge\ESI_AI_Helpdesk_Backend\ESI_AI_Helpdesk_Backend> 
