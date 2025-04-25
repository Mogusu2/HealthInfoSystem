from typing import Optional, List
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class ClientAuth(BaseModel):
    email: str
    password: str


class ProgramBase(BaseModel):
    name: str
    description: Optional[str] = None


class ProgramCreate(ProgramBase):
    pass


class ProgramRead(ProgramBase):
    id: int

    class Config:
        orm_mode = True


class ClientBase(BaseModel):
    name: str
    age: int
    contact: str



class ClientCreate(ClientBase):
    pass

class ClientRead(ClientBase):
    id: int

    class Config:
        orm_mode = True


class ClientProfile(ClientRead):
    programs: List[ProgramRead] = []


class EnrollRequest(BaseModel):
    client_id: int
    program_ids: List[int]