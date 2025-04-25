from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import engine
from app.schemas.schemas import ProgramCreate, ProgramRead
from app.models.models import HealthProgram
from app.crud import create_program


router = APIRouter(prefix="/programs", tags=["programs"])


def get_session():
    with Session(engine) as session:
        yield session
        
        
        
@router.post("/", response_model=ProgramRead)
def add_program(program: ProgramCreate, session: Session = Depends(get_session)):
    return create_program(session, HealthProgram(**program.dict()))        
        