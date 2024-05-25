from pydantic import BaseModel


class PortfolioBase(BaseModel):
    name: str


class PortfolioCreate(PortfolioBase):
    pass


class Portfolio(PortfolioBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
