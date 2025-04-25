from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import engine
from app.schemas.schemas import ClientCreate, ClientRead, ClientProfile, ProgramRead
from app.models.models import Client
from app.crud import create_client, get_client_by_id, search_clients
from app.routers.auth import get_current_client
from app.models.models import Client as ClientModel


router = APIRouter(prefix="/clients", tags=["clients"])


def get_session():
    with Session(engine) as session:
        yield session
        
        
@router.post("/", response_model=ClientRead)
def register_client(client: ClientCreate, session: Session = Depends(get_session)):
    return create_client(session, Client(**client.dict()))    



@router.get("/search", response_model=list[ClientRead])
def find_clients(q: str, session: Session = Depends(get_session)):
    return search_clients(session, q)



@router.get("/{client_id}", response_model=ClientProfile)
def get_profile(client_id: int, session: Session = Depends(get_session), current_user: ClientModel = Depends(get_current_client)):
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
