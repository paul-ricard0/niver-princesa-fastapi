# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
from models import Convidados

app = FastAPI()

# Dependency to get a DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for request/response validation
class CreateConvidado(BaseModel):
    name: str
    email: str
    phone: str
    created_at: str
    updated_at: str

class ConvidadoResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True

@app.post("/convidados", response_model=ConvidadoResponse)
def create_convidado(convidado: CreateConvidado, db: Session = Depends(get_db)):
    db_convidado = Convidados(**convidado.model_dump())
    db.add(db_convidado)
    db.commit()
    db.refresh(db_convidado)
    return db_convidado

@app.get("/convidados", response_model=list[ConvidadoResponse])
def get_convidados(db: Session = Depends(get_db)):
    convidados = db.query(Convidados).all()
    return convidados

