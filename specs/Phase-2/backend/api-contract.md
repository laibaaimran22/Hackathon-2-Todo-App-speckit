# API Contract: Phase 2 Backend

All endpoints require a `Bearer <JWT>` token in the `Authorization` header.

## Base URL
`/api`

## Endpoints

### 1. List Tasks
- **URL:** `GET /tasks`
- **Description:** Retrieve all tasks for the authenticated user.
- **Success Response:** `200 OK`
  ```json
  [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "is_completed": false,
      "created_at": "2026-01-02T10:00:00Z"
    }
  ]
  ```

### 2. Create Task
- **URL:** `POST /tasks`
- **Body:**
  ```json
  {
    "title": "Finish project",
    "description": "Complete the backend spec"
  }
  ```
- **Success Response:** `201 Created`

### 3. Get Task Details
- **URL:** `GET /tasks/{id}`
- **Success Response:** `200 OK`
- **Error Response:** `404 Not Found` (if task doesn't exist or isn't owned by user)

### 4. Update Task
- **URL:** `PUT /tasks/{id}`
- **Body:**
  ```json
  {
    "title": "Finish project (Updated)",
    "description": "Revised description",
    "is_completed": true
  }
  ```
- **Success Response:** `200 OK`

### 5. Delete Task
- **URL:** `DELETE /tasks/{id}`
- **Success Response:** `204 No Content`

### 6. Toggle Completion
- **URL:** `PATCH /tasks/{id}/complete`
- **Body:** (None required, toggles current state or explicitly sets via query param)
- **Success Response:** `200 OK`
  ```json
  {
    "id": 1,
    "is_completed": true
  }
  ```

## Security & Authentication
- **Header:** `Authorization: Bearer <TOKEN>`
- **Secret:** `BETTER_AUTH_SECRET`
- **Algorithm:** HS256
- **Validation:**
  - Token must be valid (not expired, correct signature).
  - Claims must contain `sub` representing the unique user identifier.

## Common Error Responses

| Status Code | Reason | Example Message |
|-------------|--------|-----------------|
| `401` | Missing or expired token | `{"detail": "Could not validate credentials"}` |
| `403` | Accessing other user's task | `{"detail": "Not authorized to access this resource"}` |
| `404` | Task ID does not exist | `{"detail": "Task not found"}` |
| `422` | Validation Error (Pydantic) | `{"detail": [{"loc": ["body", "title"], "msg": "field required"}]}` |
