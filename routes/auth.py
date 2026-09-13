from fastapi import APIRouter, HTTPException, status, Depends
from models import schemas
from database.supabase_client import supabase

router = APIRouter(prefix="/auth", tags=["Auth"])

def check_supabase():
    if not supabase:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Supabase credentials not configured."
        )

@router.post("/signup")
async def signup(credentials: schemas.UserCredentials):
    check_supabase()
    try:
        res = supabase.auth.sign_up({
            "email": credentials.email,
            "password": credentials.password
        })
        return {"message": "User created successfully", "user": res.user}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login")
async def login(credentials: schemas.UserCredentials):
    check_supabase()
    try:
        res = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        return {"access_token": res.session.access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.post("/logout")
async def logout():
    check_supabase()
    # While supabase-py does not support passing a specific JWT to sign_out,
    # the client library state manages the current session.
    # In a true stateless proxy, the backend shouldn't maintain state, 
    # but we can instruct the client to discard the token.
    try:
        supabase.auth.sign_out()
        return {"message": "Logged out successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
