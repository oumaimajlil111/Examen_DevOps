from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas, database

app = FastAPI(title="Ticket Management API - Unified DevSecOps")

# Create database tables if they don't exist
models.Base.metadata.create_all(bind=database.engine)


@app.post("/tickets/", response_model=schemas.Ticket, status_code=201)
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(database.get_db)):
    db_ticket = models.Ticket(
        title=ticket.title,
        description=ticket.description,
        username=ticket.username
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


@app.get("/tickets/", response_model=List[schemas.Ticket])
def read_tickets(
    status: Optional[str] = Query(None, description="Filter tickets by status"),
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Ticket)
    if status:
        allowed_statuses = ["Ouvert", "En cours", "Résolu", "Fermé"]
        if status not in allowed_statuses:
            raise HTTPException(status_code=400, detail="Invalid status filter")
        query = query.filter(models.Ticket.status == status)
    return query.all()


# --- STUDENT B WORKSPACE: AGENT STATUS ROUTING & RESPONSES ---
@app.put("/tickets/{ticket_id}", response_model=schemas.Ticket)
def update_ticket_status(
    ticket_id: int,
    update_data: schemas.TicketUpdate,
    db: Session = Depends(database.get_db)
):
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket non trouvé")

    allowed_statuses = ["Ouvert", "En cours", "Résolu", "Fermé"]
    if update_data.status not in allowed_statuses:
        raise HTTPException(status_code=400, detail="Statut invalide")

    db_ticket.status = update_data.status
    db_ticket.response = update_data.response

    db.commit()
    db.refresh(db_ticket)
    return db_ticket
