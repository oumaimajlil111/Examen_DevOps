from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict

class TicketBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Literal["High", "Medium", "Low"]

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    status: str
    response: Optional[str] = None

class TicketResponse(TicketBase):
    id: int
    status: str
    response: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
