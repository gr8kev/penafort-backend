from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Add the import for CORSMiddleware
from routes import router  # Import the router from routes.py
from database import Base, engine

# Create the FastAPI app
app = FastAPI(docs_url="/docs")


# Allow all origins for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (you can restrict this to specific domains later)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include the router with user-related routes
app.include_router(router)

# Create the database tables (only needed once during setup)
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}
