from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


class Enrollment(SQLModel, table=True):
    client_id: Optional[int] = Field(default=None, foreign_key="client.id", primary_key=True)
    program_id: Optional[int] = Field(default=None, foreign_key="healthprogram.id", primary_key=True)


class HealthProgram(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None

    enrolled_clients: List["Client"] = Relationship(
        back_populates="enrolled_programs",
        link_model=Enrollment
    )


class Client(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    contact: str
    email: str = Field(index=True, unique=True)
    hashed_password: str

    enrolled_programs: List[HealthProgram] = Relationship(
        back_populates="enrolled_clients",
        link_model=Enrollment
    )

