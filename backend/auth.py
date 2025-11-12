import os
import uuid
import requests
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from models import User, UserSession, SessionData

# Emergent Auth URL
EMERGENT_AUTH_URL = "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data"

# Database will be passed from server.py
db = None

def set_database(database):
    """Set the database instance from server.py"""
    global db
    db = database

async def process_google_session(session_id: str) -> SessionData:
    """
    Process session_id from Emergent Google OAuth and create user session.
    """
    try:
        # Get user data from Emergent Auth
        headers = {"X-Session-ID": session_id}
        response = requests.get(EMERGENT_AUTH_URL, headers=headers, timeout=10)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session ID"
            )
        
        user_data = response.json()
        user_id = user_data.get("id")
        email = user_data.get("email")
        name = user_data.get("name")
        picture = user_data.get("picture")
        
        if not user_id or not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user data from auth service"
            )
        
        # Check if user exists, if not create
        existing_user = await db.users.find_one({"_id": user_id})
        if not existing_user:
            user = User(
                id=user_id,
                email=email,
                name=name,
                picture=picture
            )
            await db.users.insert_one(user.dict(by_alias=True))
        
        # Create new session token
        session_token = f"session_{uuid.uuid4().hex}"
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        
        session = UserSession(
            id=f"sess_{uuid.uuid4().hex}",
            user_id=user_id,
            session_token=session_token,
            expires_at=expires_at
        )
        
        await db.user_sessions.insert_one(session.dict(by_alias=True))
        
        return SessionData(
            id=user_id,
            email=email,
            name=name,
            picture=picture,
            session_token=session_token
        )
        
    except requests.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Auth service unavailable: {str(e)}"
        )

async def get_current_user(request: Request) -> User:
    """
    Get current authenticated user from session token.
    Checks both cookie and Authorization header.
    """
    # Try to get token from cookie first
    session_token = request.cookies.get("session_token")
    
    # Fallback to Authorization header
    if not session_token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            session_token = auth_header.replace("Bearer ", "")
    
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    # Find session
    session = await db.user_sessions.find_one({"session_token": session_token})
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session"
        )
    
    # Check expiry
    if session["expires_at"] < datetime.now(timezone.utc):
        await db.user_sessions.delete_one({"_id": session["_id"]})
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired"
        )
    
    # Get user
    user_doc = await db.users.find_one({"_id": session["user_id"]})
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return User(**user_doc)

async def logout_user(session_token: str):
    """
    Logout user by deleting session.
    """
    result = await db.user_sessions.delete_one({"session_token": session_token})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

def create_session_cookie(response: JSONResponse, session_token: str):
    """
    Create httpOnly session cookie.
    """
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=7 * 24 * 60 * 60,  # 7 days
        path="/"
    )

def clear_session_cookie(response: JSONResponse):
    """
    Clear session cookie.
    """
    response.delete_cookie(
        key="session_token",
        path="/",
        samesite="none"
    )
