from fastapi import APIRouter, HTTPException, status, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database.supabase_client import supabase

router = APIRouter(tags=["Protected"])
public_router = APIRouter(tags=["Public"])
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    if not supabase:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Supabase credentials not configured."
        )
    token = credentials.credentials
    try:
        user_resp = supabase.auth.get_user(token)
        if not user_resp or not user_resp.user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return user_resp.user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

@router.get("/protected/profile")
async def get_profile(current_user = Depends(get_current_user)):
    return {
        "message": "Access granted to protected route",
        "user_id": current_user.id,
        "email": current_user.email,
        "metadata": current_user.user_metadata
    }

@public_router.get("/public/info")
async def get_public_info():
    return {
        "message": "This is public data, anyone can read this without a token."
    }
