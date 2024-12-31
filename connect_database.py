import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from dotenv import load_dotenv


load_dotenv()


uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")

def connect_to_database():
    """Connect to MongoDB and verify the connection."""
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)  
        client.admin.command('ping')  
        print(f"Successfully connected to MongoDB database: {db_name}")
        return client
    except ServerSelectionTimeoutError as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise RuntimeError("Failed to connect to the database")
