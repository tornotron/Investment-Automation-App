from pydantic import BaseModel


class PSUListing(BaseModel):
    id: int
    ticker: str
    index: str
    provider: str

    class Config:
        from_attributes = True
