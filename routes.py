# routes.py

from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from database import get_db, User, hash_password, verify_password

router = APIRouter()

# User registration route (updated to include more fields)
@router.post("/register")
def register(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    phone_number: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Check if the passwords match
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Check if the email is already registered
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = hash_password(password)

    # Create a new user instance
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        password=hashed_password
    )

    # Save the user to the database
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User registered successfully"}

# User login route
@router.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    # Find the user by email
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful"}
