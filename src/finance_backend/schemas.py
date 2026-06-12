from pydantic import BaseModel


class WatchlistItemCreate(BaseModel):
    ticker: str
    company_name: str | None = None
    notes: str | None = None


class FinanceNoteCreate(BaseModel):
    ticker: str
    title: str
    content: str
