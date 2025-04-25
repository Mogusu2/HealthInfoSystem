from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import engine
from app.crud import get_client_by_id
from app.schemas.schemas import ClientProfile, ProgramRead


router = APIRouter(prefix="/public", tags=["Public API"])

def get_session():
    with Session(engine) as session:
        yield session
        
        
@router.get("/client/{client_id}", response_model=ClientProfile)
def public_profile(client_id: int, session: Session = Depends(get_session)):
    client = get_client_by_id(session, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    return ClientProfile(
        id=client.id,
        name=client.name,
        age=client.age,
        contact=client.contact,
        programs=[ProgramRead.from_orm(p) for p in client.enrolled_programs]
    )        