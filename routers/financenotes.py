from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import FinanceNote
from database import SessionLocal

router = APIRouter(prefix="/financenotes", tags=["financenotes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class Finance(BaseModel):  
    ticker: str
    title: str
    content: str  


@router.get("/", status_code=200)
def read_finance_notes(db: db_dependency):
    return db.query(FinanceNote).all()


@router.get("/{finance_note_id}", status_code=200)
def read_finance_note_by_id(db: db_dependency, finance_note_id: int = Path(gt=0)):
    finance_note = db.query(FinanceNote).filter(FinanceNote.id == finance_note_id).first()
    if finance_note is None:
        raise HTTPException(status_code=404, detail="Finance note not found")
    return finance_note


@router.post("/")
def create_finance_note(db: db_dependency, finance_note_request: Finance):  
    finance_note_model = FinanceNote(**finance_note_request.model_dump())
    db.add(finance_note_model)
    db.commit()
    db.refresh(finance_note_model)  
    return finance_note_model

@router.put("/{finance_note_id}")
def update_finance_note(db: db_dependency, finance_note_id: int, finance_note_request: Finance):  
    finance_note = db.query(FinanceNote).filter(FinanceNote.id == finance_note_id).first()
    if finance_note:
        finance_note.ticker = finance_note_request.ticker
        finance_note.title = finance_note_request.title
        finance_note.content = finance_note_request.content
        db.commit()
        db.refresh(finance_note)  
        return finance_note

    else:
        raise HTTPException(status_code=404, detail="Finance note not found")
    

@router.delete("/{finance_note_id}")
def delete_finance_note(
    db: db_dependency,
    finance_note_id: int,
):
    finance_note = db.query(FinanceNote).filter(FinanceNote.id == finance_note_id).first()
    if finance_note:
        db.delete(finance_note)
        db.commit()
        return {"message": "Finance note deleted successfully"}  
    else:
        raise HTTPException(status_code=404, detail="Finance note not found")   
