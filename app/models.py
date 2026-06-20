from sqlalchemy import Column, Integer, String
from app.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    username = Column(String, nullable=False)
    # Status values: Ouvert, En cours, Résolu, Fermé
    status = Column(String, default="Ouvert", nullable=False)
    response = Column(String, nullable=True)  # Response message from agent