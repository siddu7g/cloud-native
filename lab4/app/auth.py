"""Development JWT-style authentication."""
from fastapi import Header, HTTPException

DEV_TOKEN = "dev-token"


async def require_auth(authorization: str | None = Header(default=None)):
    """Require valid Bearer token. Returns nothing if valid; raises 401 otherwise."""
    if authorization is None:
        raise HTTPException(
            status_code=401,
            detail={"error": "Authorization header is missing"},
        )
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail={"error": "Invalid Authorization header format"},
        )
    token = authorization[7:].strip()
    if token != DEV_TOKEN:
        raise HTTPException(
            status_code=401,
            detail={"error": "Invalid or expired token"},
        )
