from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Add the import for CORSMiddleware
from routes import router  # Import the router from routes.py
from database import Base, engine

# Create the FastAPI app
app = FastAPI(docs_url="/docs")


# Allow all origins for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


app.include_router(router)


Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}