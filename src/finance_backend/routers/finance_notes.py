from fastapi import APIRouter, HTTPException, Path

from ..dependencies import DBSession
from ..models import FinanceNote
from ..schemas import FinanceNoteCreate

router = APIRouter(prefix="/financenotes", tags=["financenotes"])


@router.get("/", status_code=200)
def read_finance_notes(db: DBSession):
    return db.query(FinanceNote).all()


@router.get("/{finance_note_id}", status_code=200)
def read_finance_note_by_id(db: DBSession, finance_note_id: int = Path(gt=0)):
    finance_note = (
        db.query(FinanceNote).filter(FinanceNote.id == finance_note_id).first()
    )
    if finance_note is None:
        raise HTTPException(status_code=404, detail="Finance note not found")
    return finance_note


@router.post("/")
def create_finance_note(db: DBSession, finance_note_request: FinanceNoteCreate):
    finance_note_model = FinanceNote(**finance_note_request.model_dump())
    db.add(finance_note_model)
    db.commit()
    db.refresh(finance_note_model)
    return finance_note_model


@router.put("/{finance_note_id}")
def update_finance_note(
    db: DBSession,
    finance_note_id: int,
    finance_note_request: FinanceNoteCreate,
):
    finance_note = (
        db.query(FinanceNote).filter(FinanceNote.id == finance_note_id).first()
    )
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
    db: DBSession,
    finance_note_id: int,
):
    finance_note = (
        db.query(FinanceNote).filter(FinanceNote.id == finance_note_id).first()
    )
    if finance_note:
        db.delete(finance_note)
        db.commit()
        return {"message": "Finance note deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Finance note not found")
