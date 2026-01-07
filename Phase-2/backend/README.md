# Todo Evolution Backend

## Hugging Face Spaces Deployment

This is the backend for the Todo Evolution application, designed for deployment on Hugging Face Spaces using Docker.

## Environment Variables Required

You need to set the following environment variables:

- `DATABASE_URL`: PostgreSQL database URL (e.g., your Neon database URL)
- `JWT_SECRET` or `BETTER_AUTH_SECRET`: Secret for JWT token verification (should match frontend)
- `CORS_ORIGINS`: Comma-separated list of allowed origins (e.g., your frontend URL)
- `PORT`: Port number (default: 8000)

## API Endpoints

- `GET /health` - Health check endpoint
- `GET /api/tasks` - Get user's tasks
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task

## Authentication

The backend uses JWT tokens from Better Auth for authentication. The tokens are verified using the shared secret.

## Docker Build

To build the Docker image locally:

```bash
docker build -t todo-backend .
```

To run locally:

```bash
docker run -p 8000:8000 -e DATABASE_URL="your_db_url" -e JWT_SECRET="your_secret" todo-backend
```