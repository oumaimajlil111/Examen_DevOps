from sqlalchemy import Column, Integer, String, Text
from .database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    priority = Column(String, nullable=False)  # "High", "Medium", "Low"
    status = Column(String, nullable=False, default="Ouvert")  # "Ouvert", "En cours", "Résolu", "Fermé"
    response = Column(String, nullable=True)  # Managed by Student B
