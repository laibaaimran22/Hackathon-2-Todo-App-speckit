# Todo Evolution Backend - Phase 3

## Hugging Face Spaces Deployment

This is the backend for the Todo Evolution application, designed for deployment on Hugging Face Spaces using Docker. This backend supports AI chatbot integration via Model Context Protocol (MCP).

## Environment Variables Required

You need to set the following environment variables:

- `DATABASE_URL`: PostgreSQL database URL (e.g., your Neon database URL)
- `JWT_SECRET` or `BETTER_AUTH_SECRET`: Secret for JWT token verification (should match frontend)
- `CORS_ORIGINS`: Comma-separated list of allowed origins (e.g., your frontend URL, Hugging Face Space URL)
- `COHERE_API_KEY`: Your Cohere API key for AI chatbot functionality
- `PORT`: Port number (default: 8000)

## API Endpoints

### Task Management
- `GET /health` - Health check endpoint
- `GET /api/tasks` - Get user's tasks
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/{id}` - Update a task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion status
- `DELETE /api/tasks/{id}` - Delete a task

### MCP (Model Context Protocol) Server for AI Chatbot
- `GET /mcp/tools` - Get available tools for the AI agent
- `POST /mcp/call-tools` - Execute tools requested by the AI agent

## Authentication

The backend uses JWT tokens from Better Auth for authentication. The tokens are verified using the shared secret.

## MCP Server Capabilities

The MCP server exposes the following tools to the AI chatbot:
- `add_task`: Add a new task to the user's list
- `get_tasks`: Retrieve the user's tasks
- `update_task`: Update an existing task
- `delete_task`: Delete a task
- `mark_complete`: Toggle the completion status of a task

## Hugging Face Spaces Setup

1. Create a new Space on Hugging Face with the "Docker" SDK option
2. Set the required environment variables in the Space settings
3. Add the following files to your repository:
   - `Dockerfile`
   - `requirements.txt`
   - `main.py`
   - `mcp/` directory containing the MCP server implementation
4. The Space will automatically build and deploy the application

## Docker Build

To build the Docker image locally:

```bash
docker build -t todo-backend .
```

To run locally:

```bash
docker run -p 8000:8000 \
  -e DATABASE_URL="your_db_url" \
  -e JWT_SECRET="your_secret" \
  -e COHERE_API_KEY="your_cohere_key" \
  -e CORS_ORIGINS="http://localhost:3000,https://your-frontend-url.vercel.app" \
  todo-backend
```