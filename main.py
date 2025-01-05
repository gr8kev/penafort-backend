from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from connect_database import connect_to_database  
from routes import router as routes_router  


app = FastAPI(docs_url="/docs")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    connect_to_database()


app.include_router(routes_router, prefix="/api", tags=["Authentication"])

# Root endpoint (for testing the app)
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}