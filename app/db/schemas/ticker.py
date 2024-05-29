from pydantic import BaseModel


class Ticker(BaseModel):
    ticker: str
    name: str
    exchange: str
    category_name: str
    country: str
    provider: str

    class Config:
        orm_mode = True


class Message(BaseModel):
    message: str
