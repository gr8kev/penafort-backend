from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from database import get_db, User, hash_password, verify_password
from pydantic import EmailStr
import re

router = APIRouter()


def validate_password(password: str):
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
    if not re.search(r"[A-Z]", password):
        raise HTTPException(status_code=400, detail="Password must include at least one uppercase letter")
    if not re.search(r"\d", password):
        raise HTTPException(status_code=400, detail="Password must include at least one number")

# User registration route
@router.post("/register")
def register(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: EmailStr = Form(...),  
    phone_number: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    
    validate_password(password)

    
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    
    hashed_password = hash_password(password)

    
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        password=hashed_password
    )

    
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User registered successfully", "user_id": user.id}


@router.post("/login")
def login(email: EmailStr = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    
    token = "jwt-token-placeholder"

    return {"message": "Login successful", "token": token}


@router.get("/users", tags=["Users"])
def get_users(db: Session = Depends(get_db)):
    """
    Fetch a list of all users.
    """
    users = db.query(User).all()
    user_list = [
        {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone_number": user.phone_number,
        }
        for user in users
    ]
    return {"total_users": len(users), "users": user_list}
@router.get("/admin/users", tags=["Admin"])
def admin_get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": user.id, "email": user.email} for user in users]

