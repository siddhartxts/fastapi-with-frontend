from fastapi import APIRouter, HTTPException, Path

from ..dependencies import DBSession
from ..models import WatchlistItem
from ..schemas import WatchlistItemCreate

router = APIRouter(prefix="/watchlist", tags=["watchlist"])


@router.get("/", status_code=200)
def read_watchlist(db: DBSession):
    return db.query(WatchlistItem).all()


@router.get("/{watchlist_item_id}", status_code=200)
def read_watchlist_item_by_id(db: DBSession, watchlist_item_id: int = Path(gt=0)):
    return db.query(WatchlistItem).filter(WatchlistItem.id == watchlist_item_id).first()


@router.post("/")
def create_watchlist_item(db: DBSession, watchlist_item_request: WatchlistItemCreate):
    watchlist_item_model = WatchlistItem(**watchlist_item_request.model_dump())
    db.add(watchlist_item_model)
    db.commit()
    return watchlist_item_model


@router.put("/{watchlist_item_id}")
def update_watchlist_item(
    db: DBSession,
    watchlist_item_id: int,
    watchlist_item_request: WatchlistItemCreate,
):
    watchlist_item = (
        db.query(WatchlistItem).filter(WatchlistItem.id == watchlist_item_id).first()
    )
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
    db: DBSession,
    watchlist_item_id: int,
):
    watchlist_item = (
        db.query(WatchlistItem).filter(WatchlistItem.id == watchlist_item_id).first()
    )
    if watchlist_item:
        db.delete(watchlist_item)
        db.commit()
        return {"message": "Watchlist item deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Watchlist item not found")
