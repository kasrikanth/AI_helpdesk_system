# ESI AI Helpdesk Backend

## Overview
The ESI AI Helpdesk Backend is a robust application designed to support helpdesk operations by leveraging AI capabilities. It provides various functionalities to manage tickets, authenticate users, and integrate with large language models (LLMs) for intelligent responses and escalations.

## Features
- **User Authentication**: Secure login and role-based access control.
- **Ticket Management**: Create, update, and track helpdesk tickets.
- **Knowledge Base Integration**: Retrieve and manage knowledge base articles.
- **AI-Powered Escalation**: Classify and escalate tickets using AI models.
- **Metrics and Reporting**: Generate insights and reports on helpdesk performance.

## User Roles
The application supports the following user roles:

1. **Admin**:
   - Manage user roles and permissions.
   - Oversee system configurations.
2. **Helpdesk Agent**:
   - Handle tickets and respond to user queries.
   - Escalate issues when necessary.
3. **End User**:
   - Submit tickets for issues or queries.
   - Track the status of submitted tickets.

## Application Structure
The backend application is organized into the following modules:

- **APIs**: Contains endpoints for authentication, ticket management, and metrics.
- **LLM Services**: Includes logic for AI-based ticket classification and retrieval-augmented generation (RAG).
- **Models**: Defines database schemas and ORM models.
- **Utils**: Provides utility functions for configuration, security, and dependencies.

## How to Use
1. **Setup**:
   - Install dependencies using `pip install -r requirements.txt`.
   - Initialize the database using `python -m app.init_db`.
   - Seed roles using `python -m app.seed_roles`.
2. **Run the Application**:
   - Start the server with `uvicorn app.main:app --reload`.
3. **Access the APIs**:
   - Use tools like Postman or Swagger UI to interact with the endpoints.

## Knowledge Base
The application integrates with a knowledge base stored in the `kbs/` directory. This includes articles on various topics such as authentication, troubleshooting, and escalation policies.

## Future Enhancements
- Add support for multi-language ticket handling.
- Implement advanced analytics dashboards.
- Enhance AI models for better ticket classification and response generation.