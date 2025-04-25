from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import engine
from app.schemas.schemas import EnrollRequest
from app.crud import enroll_client, get_client_by_id, get_program_by_id


router = APIRouter(prefix="/enrollments", tags=["enrollments"])


def get_session():
    with Session(engine) as session:
        yield session
        
        
        
@router.post("/")
def enroll(enroll_request: EnrollRequest, session: Session = Depends(get_session)):
    client = get_client_by_id(session, enroll_request.client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    for pid in enroll_request.program_ids:
        if not get_program_by_id(session, pid):
            raise HTTPException(status_code=404, detail=f"Program ID {pid} not found")

    enroll_client(session, enroll_request.client_id, enroll_request.program_ids)
    return {"message": "Client enrolled successfully"}