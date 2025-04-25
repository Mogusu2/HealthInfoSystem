from sqlmodel import SQLModel, Session
from app.database import engine
from app.models.models import Client, HealthProgram, Enrollment

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()
