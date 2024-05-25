from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import schemas, crud
from app.api.v1.dependencies import get_db
from typing import List

router = APIRouter()


@router.post("/", response_model=schemas.Portfolio)
def create_portfolio(
    owner_id: int, portfolio: schemas.PortfolioCreate, db: Session = Depends(get_db)
):
    return crud.create_portfolio(db=db, portfolio=portfolio, owner_id=owner_id)


@router.get("/", response_model=List[schemas.Portfolio])
def read_portfolios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    portfolios = crud.get_portfolios(db, skip=skip, limit=limit)
    return portfolios


@router.get("/{portfolio_id}", response_model=schemas.Portfolio)
def read_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    db_portfolio = crud.get_portfolio(db, portfolio_id=portfolio_id)
    if db_portfolio is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return db_portfolio
