from fastapi import APIRouter, HTTPException, Form, Depends
from pydantic import EmailStr
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from database import create_user, get_user, verify_password, blacklist_token, is_token_blacklisted  

load_dotenv()

router = APIRouter()


SECRET_KEY = os.getenv("SECRET_KEY", "default_fallback_key")  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    """Create a JWT token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_token(token: str):
    """Verify and decode the JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None or is_token_blacklisted(token):
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/register")
def register(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: EmailStr = Form(...),
    phone_number: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
):
    
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    
    existing_user = get_user(email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")


    create_user(
        username=email,  
        password=password,  
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number
    )

    return {"message": "User registered successfully"}


@router.post("/login")
def login(email: EmailStr = Form(...), password: str = Form(...)):
    user = get_user(email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not verify_password(password, user['password']):
        raise HTTPException(status_code=401, detail="Incorrect password")

    
    token = create_access_token({"sub": email})
    
    return {"message": "Login successful", "token": token}


@router.post("/logout")
def logout(token: str = Depends(authenticate_token)):
    """Blacklist the token and log the user out."""
    blacklist_token(token)
    return {"message": "Logged out successfully"}