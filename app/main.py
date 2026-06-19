from typing import List, Optional
from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, Base, get_db

# Automatically create the SQLite database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ticket Management API",
    description="Backend Core for the Ticket System",
    version="1.0.0"
)

@app.post("/tickets/", response_model=schemas.TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    db_ticket = models.Ticket(
        title=ticket.title,
        description=ticket.description,
        priority=ticket.priority,
        status="Ouvert",
        response=None
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

@app.get("/tickets/", response_model=List[schemas.TicketResponse])
def read_tickets(status: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Ticket)
    if status:
        query = query.filter(models.Ticket.status == status)
    return query.all()
