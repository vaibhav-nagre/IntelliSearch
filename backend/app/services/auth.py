from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Dict, Optional
import httpx

from app.config import get_settings

settings = get_settings()
security = HTTPBearer()


async def verify_google_token(token: str) -> Dict:
    """Verify Google ID token"""
    try:
        # Verify with Google's token verification endpoint
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
            )
            
            if response.status_code == 200:
                token_info = response.json()
                
                # Verify audience (client ID)
                if token_info.get("aud") != settings.google_client_id:
                    raise HTTPException(status_code=401, detail="Invalid token audience")
                
                # Extract user information
                return {
                    "user_id": token_info.get("sub"),
                    "email": token_info.get("email"),
                    "name": token_info.get("name"),
                    "groups": token_info.get("groups", []),  # Custom claim
                    "is_admin": token_info.get("admin", False)  # Custom claim
                }
            else:
                raise HTTPException(status_code=401, detail="Invalid token")
                
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {str(e)}")


def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    
    return encoded_jwt


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """Verify JWT token"""
    try:
        payload = jwt.decode(
            credentials.credentials, 
            settings.secret_key, 
            algorithms=[settings.algorithm]
        )
        
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return payload
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_user(token_data: Dict = Depends(verify_token)) -> Dict:
    """Get current user from token"""
    # In production, you might want to fetch fresh user data from database
    return {
        "user_id": token_data.get("sub"),
        "email": token_data.get("email"),
        "name": token_data.get("name"),
        "groups": token_data.get("groups", []),
        "is_admin": token_data.get("is_admin", False)
    }


async def get_admin_user(current_user: Dict = Depends(get_current_user)) -> Dict:
    """Require admin user"""
    if not current_user.get("is_admin", False):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return current_user
