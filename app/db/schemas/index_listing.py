from pydantic import BaseModel


class IndexListing(BaseModel):
    id: int
    ticker: str
    index: str
    provider: str

    class Config:
        from_attributes = True
