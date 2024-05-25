from pydantic import BaseModel


class TradeBase(BaseModel):
    asset: str
    quantity: float
    price: float
    trade_type: str


class TradeCreate(TradeBase):
    portfolio_id: int


class Trade(TradeBase):
    id: int
    portfolio_id: int

    class Config:
        from_attributes = True
