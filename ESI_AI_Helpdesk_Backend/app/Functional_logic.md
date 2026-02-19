# Functional Logic

## Role Creation Logic

### Current Implementation

**Super Admin Can Create:**
- admin
- support_engineer
- operator
- trainee
- instructor

**Admin Can Create:**
- support_engineer
- operator
- trainee
- instructor

**Restrictions:**
- Super Admin and Admin roles cannot be created by Admin.

## Functional Flow of APIs

### Authentication APIs
1. **Login**:
   - Endpoint: `/auth/login`
   - Validates user credentials and generates JWT tokens.
2. **Register**:
   - Endpoint: `/auth/register`
   - Allows new users to register (restricted to certain roles).
3. **Role Management**:
   - Endpoint: `/auth/roles`
   - Manages role creation and assignment.

### Ticket Management APIs
1. **Create Ticket**:
   - Endpoint: `/tickets/create`
   - Allows users to create a new ticket.
2. **Update Ticket**:
   - Endpoint: `/tickets/update/{ticket_id}`
   - Enables agents to update ticket details.
3. **View Tickets**:
   - Endpoint: `/tickets/view`
   - Retrieves a list of tickets based on user roles.

### Metrics APIs
1. **Get Metrics**:
   - Endpoint: `/metrics`
   - Provides performance metrics for the helpdesk system.

### Knowledge Base APIs
1. **Search Knowledge Base**:
   - Endpoint: `/kb/search`
   - Allows users to search for articles in the knowledge base.
2. **Add Article**:
   - Endpoint: `/kb/add`
   - Enables admins to add new articles to the knowledge base.

### AI Services APIs
1. **Classify Ticket**:
   - Endpoint: `/ai/classify`
   - Uses AI to classify ticket priority and category.
2. **Escalate Ticket**:
   - Endpoint: `/ai/escalate`
   - Determines if a ticket needs escalation based on AI analysis.