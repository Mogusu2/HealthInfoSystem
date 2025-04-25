from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import clients, programs, enrollments

app = FastAPI(title="Health Information System")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(clients.router)
app.include_router(programs.router)
app.include_router(enrollments.router)
