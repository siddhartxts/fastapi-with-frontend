from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import WatchlistItem
from database import SessionLocal

router = APIRouter(prefix="/watchlist", tags=["watchlist"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class Watch(BaseModel):
    ticker: str
    company_name: str | None = None
    notes: str | None = None


@router.get("/", status_code=200)
def read_watchlist(db: db_dependency):
    return db.query(WatchlistItem).all()


@router.get("/{watchlist_item_id}", status_code=200)
def read_watchlist_item_by_id(db: db_dependency, watchlist_item_id: int = Path(gt=0)):
    return db.query(WatchlistItem).filter(WatchlistItem.id == watchlist_item_id).first()


@router.post("/")
def create_watchlist_item(db: db_dependency, watchlist_item_request: Watch):
    watchlist_item_model = WatchlistItem(**watchlist_item_request.model_dump())
    db.add(watchlist_item_model)
    db.commit()
    return watchlist_item_model


@router.put("/{watchlist_item_id}")
def update_watchlist_item(db: db_dependency, watchlist_item_id: int, watchlist_item_request: Watch):
    watchlist_item = db.query(WatchlistItem).filter(WatchlistItem.id == watchlist_item_id).first()
    if watchlist_item:
        watchlist_item.ticker = watchlist_item_request.ticker
        watchlist_item.company_name = watchlist_item_request.company_name
        watchlist_item.notes = watchlist_item_request.notes
        db.commit()
        return watchlist_item

    else:
        raise HTTPException(status_code=404, detail="Watchlist item not found")


@router.delete("/{watchlist_item_id}")
def delete_watchlist_item(
    db: db_dependency,
    watchlist_item_id: int,
):
    watchlist_item = db.query(WatchlistItem).filter(WatchlistItem.id == watchlist_item_id).first()
    if watchlist_item:
        db.delete(watchlist_item)
        db.commit()
        return {"message": "Watchlist item deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Watchlist item not found")
