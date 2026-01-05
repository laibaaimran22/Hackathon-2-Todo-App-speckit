# REST API Design Skill

## Overview
This skill focuses on designing consistent, predictable, and scalable RESTful APIs. It emphasizes standard HTTP semantics, clear endpoint structures, and robust error handling to ensure a high-quality developer experience and seamless frontend integration.

## Core Capabilities
- **Semantic Path Design**: Using nouns and proper hierarchies for endpoints (e.g., `/tasks`, `/tasks/{id}`).
- **HTTP Method Selection**: Correct use of `GET`, `POST`, `PUT`, `PATCH`, and `DELETE`.
- **Status Code Mapping**: Returning appropriate 2xx, 4xx, and 5xx codes for every operation.
- **Payload Structuring**: Designing consistent JSON envelopes for requests and responses.
- **Resource Versioning**: Planning for API evolution through prefixing (e.g., `/api/v1/...`).

## Recommended Endpoint Structure (Todo Management)
| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| **GET** | `/tasks` | List all tasks for current user | `200 OK` |
| **POST** | `/tasks` | Create a new task | `201 Created` |
| **GET** | `/tasks/{id}` | Get specific task details | `200 OK` |
| **PATCH** | `/tasks/{id}` | Partially update task (e.g., status) | `200 OK` |
| **PUT** | `/tasks/{id}` | Replace/Update entire task | `200 OK` |
| **DELETE** | `/tasks/{id}` | Remove a task | `204 No Content` |

## Status Code Guide
- **200 OK**: Success (Generic).
- **201 Created**: Successful resource creation.
- **204 No Content**: Successful operation with no return body (e.g., Delete).
- **400 Bad Request**: Invalid input or client-side error.
- **401 Unauthorized**: Missing or invalid authentication token.
- **403 Forbidden**: Authenticated but lacks permission for specific resource.
- **404 Not Found**: Resource does not exist.
- **500 Internal Server Error**: Unexpected server failure.

## Error Response Pattern
Consistency is key for frontend error handling:
```json
{
  "error": {
    "code": "TASK_NOT_FOUND",
    "message": "Task with ID 123 does not exist.",
    "details": {}
  }
}
```

## Best Practices
1.  **Nouns over Verbs**: Use `/tasks` instead of `/getTasks`.
2.  **Pluralization**: Use plural nouns for resource collections (e.g., `/users`, `/tasks`).
3.  **Snake Case**: Use `snake_case` for JSON keys in both requests and responses.
4.  **Filtering & Pagination**: Use query parameters for modifiers (e.g., `/tasks?status=completed&limit=10`).
5.  **Statelessness**: Every request must contain all information necessary for the server to fulfill it (e.g., Auth headers).

## Example Usage
> "Design a RESTful API contract for a multi-user todo app, including structured error responses and proper HTTP status code mapping for all CRUD operations."
