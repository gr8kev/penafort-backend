from passlib.context import CryptContext
from pymongo import MongoClient
from dotenv import load_dotenv
from fastapi import HTTPException
import os


load_dotenv()

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# MongoDB connection
def connect_to_database():
    """Connect to the MongoDB database."""
    mongo_url = os.getenv("MONGO_URI")  
    client = MongoClient(mongo_url)  
    return client


client = connect_to_database()
db_name = os.getenv("DB_NAME")
db = client[db_name]  

# Collection for 'users' in MongoDB
users_collection = db.users

# Hash a password using pbkdf2_sha256
def hash_password(password: str) -> str:
    """Hash the password using pbkdf2_sha256."""
    return pwd_context.hash(password)

# Verify a password against the stored hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify the plain-text password against the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def create_user(username: str, password: str, first_name: str, last_name: str, email: str, phone_number: str):
    """Create a new user in the MongoDB database with a hashed password."""
    hashed_password = hash_password(password)  
    user_data = {
        "username": username,
        "password": hashed_password, 
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone_number": phone_number
    }
    try:
        users_collection.insert_one(user_data)  
    except Exception as e:
        print(f"Error inserting user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def get_user(email: str):
    """Fetch a user from the MongoDB database by email."""
    try:
        user = users_collection.find_one({"email": email})
        if user:
            return user
        return None
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None
