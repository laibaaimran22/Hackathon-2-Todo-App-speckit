# Better Auth + JWT Authentication Skill

## Overview
This skill focuses on implementing a secure, shared authentication layer between a **Next.js frontend** and a **FastAPI backend** using **Better Auth** and **JWT**. It ensures that user identities are verified across service boundaries and that data access is strictly isolated.

## Core Capabilities
- **Better Auth Integration**: Configure Better Auth in Next.js with the JWT plugin to generate verifiable tokens.
- **Cross-Service JWT Verification**: Implement shared-secret or public-key verification in FastAPI to validate tokens issued by the frontend.
- **User Isolation Logic**: Extract the `user_id` (sub) from the JWT in the backend to ensure users only access their own records.
- **Middleware Protection**: Secure entire API routers using FastAPI dependencies that verify the `Authorization` header.

## Implementation Workflow

### 1. Frontend (Next.js + Better Auth)
Configure Better Auth to issue JWTs:
```typescript
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
    database: ...,
    plugins: [
        jwt({
            jwtSecret: process.env.JWT_SECRET, // Shared with backend
        })
    ]
});
```

### 2. Backend (FastAPI Verification)
Create a dependency to verify and extract the user:
```python
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
JWT_SECRET = "your-shared-secret"
ALGORITHM = "HS256"

async def get_current_user(auth: HTTPAuthorizationCredentials = Security(security)):
    try:
        payload = jwt.decode(auth.credentials, JWT_SECRET, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
```

## Best Practices
1.  **Shared Secret**: Use a strong, environment-specific secret shared only between the Next.js server and FastAPI server.
2.  **User Isolation**: Every database query in the backend should use the `user_id` extracted from the token in its `WHERE` clause.
3.  **Token Expiry**: Ensure JWTs have a short life-span and implement refresh tokens if necessary.
4.  **HTTPS Only**: Never transmit tokens over unencrypted HTTP.
5.  **Scope Validation**: Use the JWT `roles` or `scopes` if additional authorization levels (e.g., Admin) are required.

## Example Usage
> "Implement a secure connection between Next.js and FastAPI using Better Auth JWTs, ensuring all Task CRUD operations in the backend are isolated by user_id."
