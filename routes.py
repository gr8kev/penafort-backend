from fastapi import APIRouter, HTTPException, Form
from pydantic import EmailStr
from database import create_user, get_user, verify_password  
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv


load_dotenv()

router = APIRouter()

# Environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "default_fallback_key")  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Helper function to create a JWT token
def create_access_token(data: dict):
    """Create a JWT token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# User registration route
@router.post("/register")
def register(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: EmailStr = Form(...),
    phone_number: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
):
    # Check if the passwords match
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Check if the user already exists by email
    existing_user = get_user(email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create the new user in MongoDB with the hashed password
    create_user(
        username=email,  
        password=password,  
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number
    )

    return {"message": "User registered successfully"}

# User login route
@router.post("/login")
def login(email: EmailStr = Form(...), password: str = Form(...)):
    user = get_user(email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not verify_password(password, user['password']):
        raise HTTPException(status_code=401, detail="Incorrect password")

    # Generate a JWT token
    token = create_access_token({"sub": email})
    
    return {"message": "Login successful", "token": token}
