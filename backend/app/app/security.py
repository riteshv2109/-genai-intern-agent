# app/security.py
from fastapi import Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from backend.app.app.config import settings

# Define where to look for API key (Authorization header or custom header)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    """
    Dependency to secure endpoints with API Key.
    Checks against value in settings.API_KEY
    """
    if api_key == settings.api_key:
        return api_key
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Invalid or missing API Key"
    )
