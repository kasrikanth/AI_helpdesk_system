# API Documentation

## Endpoints

### Authentication
1. **Login**
   - **Endpoint**: `POST /auth/login`
   - **Description**: Authenticates a user and returns a JWT token.
   - **Request Schema**:
     ```json
     {
       "username": "string",
       "password": "string"
     }
     ```
   - **Response Schema**:
     ```json
     {
       "access_token": "string",
       "token_type": "string"
     }
     ```

2. **Register**
   - **Endpoint**: `POST /auth/register`
   - **Description**: Registers a new user.
   - **Request Schema**:
     ```json
     {
       "username": "string",
       "password": "string",
       "role": "string"
     }
     ```
   - **Response Schema**:
     ```json
     {
       "message": "User registered successfully."
     }
     ```

### Ticket Management

2. **Update Ticket**
   - **Endpoint**: `PUT /tickets/update/{ticket_id}`
   - **Description**: Updates an existing ticket.
   - **Request Schema**:
     ```json
     {
       "status": "string",
       "comments": "string"
     }
     ```
   - **Response Schema**:
     ```json
     {
       "message": "Ticket updated successfully."
     }
     ```

### Metrics
1. **Get Metrics**
   - **Endpoint**: `GET /metrics`
   - **Description**: Retrieves system performance metrics.
   - **Response Schema**:
     ```json
     {
       "total_tickets": "integer",
       "resolved_tickets": "integer",
       "pending_tickets": "integer"
     }
     ```

## Error Patterns

### Standard Error Response
- **Schema**:
  ```json
  {
    "error": {
      "code": "integer",
      "message": "string",
      "details": "string"
    }
  }
  ```

### Common Error Codes
1. **400 Bad Request**:
   - Invalid input data.
2. **401 Unauthorized**:
   - Missing or invalid authentication token.
3. **403 Forbidden**:
   - Insufficient permissions.
4. **404 Not Found**:
   - Resource not found.
5. **500 Internal Server Error**:
   - Unexpected server error.