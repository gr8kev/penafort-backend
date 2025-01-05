from passlib.context import CryptContext
from pymongo import MongoClient
from dotenv import load_dotenv
from fastapi import HTTPException
import logging
import os


load_dotenv()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# MongoDB connection
def connect_to_database():
    """Connect to the MongoDB database."""
    try:
        mongo_url = os.getenv("MONGO_URI")
        client = MongoClient(mongo_url)
        logger.info("Successfully connected to MongoDB")
        return client
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")

# Initialize MongoDB client and database
client = connect_to_database()
db_name = os.getenv("DB_NAME", "default_db_name")  # Fallback to default name
db = client[db_name]


users_collection = db.users
blacklisted_tokens_collection = db.blacklisted_tokens


def hash_password(password: str) -> str:
    """Hash the password using pbkdf2_sha256."""
    return pwd_context.hash(password)

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
        "phone_number": phone_number,
    }
    try:
        users_collection.insert_one(user_data)
        logger.info(f"User {email} created successfully")
    except Exception as e:
        logger.error(f"Error inserting user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def get_user(email: str):
    """Fetch a user from the MongoDB database by email."""
    try:
        user = users_collection.find_one({"email": email})
        return user
    except Exception as e:
        logger.error(f"Error fetching user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Token blacklist operations
def blacklist_token(token: str):
    """Add a token to the blacklist."""
    try:
        blacklisted_tokens_collection.insert_one({"token": token})
        logger.info("Token blacklisted successfully")
    except Exception as e:
        logger.error(f"Error blacklisting token: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def is_token_blacklisted(token: str):
    """Check if a token is blacklisted."""
    try:
        return blacklisted_tokens_collection.find_one({"token": token}) is not None
    except Exception as e:
        logger.error(f"Error checking token blacklist: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")