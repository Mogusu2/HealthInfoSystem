from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_db_and_tables
from app.routers import clients, programs, enrollments
from app.routers import clients, programs, enrollments, auth


app = FastAPI(title="Health Information System")


origins = [
    "http://localhost",
    "http://localhost:3000",
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(programs.router)
app.include_router(enrollments.router)
