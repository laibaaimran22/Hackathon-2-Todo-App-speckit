from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()

security = HTTPBearer()

def get_current_user_id(authorization: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Extract user ID from JWT token using shared BETTER_AUTH_SECRET.
    Verifies JWT using the same secret used by Better Auth.

    Better Auth JWT format:
    - The JWT is signed with the JWT_SECRET (or BETTER_AUTH_SECRET)
    - The user ID is typically in the 'sub' claim
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = authorization.credentials
        print(f"[DEBUG] Received token: {token[:80] if token else 'None'}...")

        if not token:
            print("[DEBUG] No token provided")
            raise credentials_exception

        # Check if this looks like a JWT (has dots)
        if '.' not in token:
            print(f"[DEBUG] Token does not appear to be a JWT (no dots found)")
            raise credentials_exception

        # Get the shared secret used by Better Auth for JWT signing
        # Check multiple possible environment variable names
        shared_secret = (
            os.getenv("BETTER_AUTH_SECRET") or
            os.getenv("better_auth_secret") or  # lowercase variant
            os.getenv("JWT_SECRET") or
            os.getenv("jwt_secret")  # lowercase variant
        )
        if not shared_secret:
            print("[DEBUG] No BETTER_AUTH_SECRET, better_auth_secret, JWT_SECRET, or jwt_secret found in environment")
            raise credentials_exception

        print(f"[DEBUG] Using secret: {shared_secret[:20]}...")

        # Decode JWT using the shared secret
        try:
            payload = jwt.decode(token, shared_secret, algorithms=["HS256"])
            print(f"[DEBUG] Decoded JWT payload keys: {list(payload.keys())}")
            print(f"[DEBUG] Full payload: {payload}")

            # Extract user ID from payload - Better Auth uses 'sub' claim
            user_id = payload.get("sub")

            if not user_id:
                # Try alternative claim names
                user_id = payload.get("userId") or payload.get("user_id")
                if user_id:
                    print(f"[DEBUG] Found user_id in alternative claim: {user_id}")

            # Check nested user object
            if not user_id and "user" in payload:
                user_obj = payload.get("user")
                if isinstance(user_obj, dict):
                    user_id = user_obj.get("id")
                elif isinstance(user_obj, str):
                    user_id = user_obj

            if not user_id:
                print(f"[DEBUG] No user ID found in JWT payload. Available keys: {list(payload.keys())}")
                raise credentials_exception

            print(f"[DEBUG] Successfully extracted user_id: {user_id}")
            return str(user_id)

        except JWTError as jwt_error:
            print(f"[DEBUG] JWT verification failed: {str(jwt_error)}")
            import traceback
            traceback.print_exc()
            raise credentials_exception

    except HTTPException:
        raise
    except Exception as e:
        print(f"[DEBUG] Auth error - Type: {type(e).__name__}, Message: {str(e)}")
        import traceback
        traceback.print_exc()
        raise credentials_exception


def get_current_user_id_from_token(token: str) -> str:
    """
    Extract user ID from JWT token using shared BETTER_AUTH_SECRET.
    This function is used by MCP tools to authenticate requests.

    Args:
        token: JWT token string

    Returns:
        str: User ID if token is valid, None otherwise
    """
    try:
        print(f"[DEBUG] Received token: {token[:80] if token else 'None'}...")

        if not token:
            print("[DEBUG] No token provided")
            return None

        # Check if this looks like a JWT (has dots)
        if '.' not in token:
            print(f"[DEBUG] Token does not appear to be a JWT (no dots found)")
            return None

        # Get the shared secret used by Better Auth for JWT signing
        # Check multiple possible environment variable names
        shared_secret = (
            os.getenv("BETTER_AUTH_SECRET") or
            os.getenv("better_auth_secret") or  # lowercase variant
            os.getenv("JWT_SECRET") or
            os.getenv("jwt_secret")  # lowercase variant
        )
        if not shared_secret:
            print("[DEBUG] No BETTER_AUTH_SECRET, better_auth_secret, JWT_SECRET, or jwt_secret found in environment")
            return None

        print(f"[DEBUG] Using secret: {shared_secret[:20]}...")

        # Decode JWT using the shared secret
        try:
            payload = jwt.decode(token, shared_secret, algorithms=["HS256"])
            print(f"[DEBUG] Decoded JWT payload keys: {list(payload.keys())}")
            print(f"[DEBUG] Full payload: {payload}")

            # Extract user ID from payload - Better Auth uses 'sub' claim
            user_id = payload.get("sub")

            if not user_id:
                # Try alternative claim names
                user_id = payload.get("userId") or payload.get("user_id")
                if user_id:
                    print(f"[DEBUG] Found user_id in alternative claim: {user_id}")

            # Check nested user object
            if not user_id and "user" in payload:
                user_obj = payload.get("user")
                if isinstance(user_obj, dict):
                    user_id = user_obj.get("id")
                elif isinstance(user_obj, str):
                    user_id = user_obj

            if not user_id:
                print(f"[DEBUG] No user ID found in JWT payload. Available keys: {list(payload.keys())}")
                return None

            print(f"[DEBUG] Successfully extracted user_id: {user_id}")
            return str(user_id)

        except JWTError as jwt_error:
            print(f"[DEBUG] JWT verification failed: {str(jwt_error)}")
            import traceback
            traceback.print_exc()
            return None

    except Exception as e:
        print(f"[DEBUG] Auth error - Type: {type(e).__name__}, Message: {str(e)}")
        import traceback
        traceback.print_exc()
        return None