from sqlmodel import Session, select
from app.models.models import Client, HealthProgram, Enrollment


# CRUD operations for Client
def create_client(session: Session, client: Client) -> Client:
    session.add(client)
    session.commit()
    session.refresh(client)
    return client



def get_client_by_id(session: Session, client_id: int) -> Client:
    return session.get(Client, client_id)


def search_clients(session: Session, keyword: str):
    statement = select(Client).where(Client.name.contains(keyword))
    return session.exec(statement).all()



# CRUD operations for HealthProgram
def create_program(session: Session, program: HealthProgram) -> HealthProgram:
    session.add(program)
    session.commit()
    session.refresh(program)
    return program


def get_program_by_id(session: Session, program_id: int) -> HealthProgram:
    return session.get(HealthProgram, program_id)



# CRUD operations for Enrollment
def enroll_client(session: Session, client_id: int, program_ids: list[int]):
    enrollments = []
    for pid in program_ids:
        enrollment = Enrollment(client_id=client_id, program_id=pid)
        session.add(enrollment)
        enrollments.append(enrollment)
    session.commit()
    return enrollments    