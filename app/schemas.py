from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal

StatusType = Literal["Ouvert", "En cours", "Résolu", "Fermé"]


class TicketCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    username: str = Field(..., min_length=1, max_length=50)


class TicketUpdate(BaseModel):
    status: str
    response: Optional[str] = None


class Ticket(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    username: str
    status: str
    response: Optional[str] = None