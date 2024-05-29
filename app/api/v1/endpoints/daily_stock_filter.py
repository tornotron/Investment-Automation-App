from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.db import schemas, crud
from app.api.v1.dependencies import get_db
from app.services.filter_daily_stocks import StockFilteringService

router = APIRouter()


@router.post("/", response_model=schemas.DailyStockFilter)
def create_stock_filter(
    stock_filter: schemas.DailyStockFilterCreate, db: Session = Depends(get_db)
):
    return crud.create_daily_stock_filter(db=db, stock_filter=stock_filter)


@router.get("/", response_model=List[schemas.DailyStockFilter])
def read_filtered_stocks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_daily_filtered_stocks(db, skip=skip, limit=limit)


@router.get("/{filter_date}", response_model=List[schemas.DailyStockFilter])
def read_filtered_stocks_by_date(filter_date: date, db: Session = Depends(get_db)):
    stocks = crud.get__daily_filtered_stocks_by_date(db, filter_date=filter_date)
    if not stocks:
        raise HTTPException(status_code=404, detail="No stocks found for this date")
    return stocks


@router.post(
    "/generate_daily_filtered_stocks", response_model=schemas.StockFilterResponse
)
def generate_daily_stock_filters(
    request: schemas.StockFilterRequest,
    db: Session = Depends(get_db),
):
    service = StockFilteringService()
    filtered_stocks = service.get_daily_filtered_stocks(request.date)

    # Convert the result to the response format
    response_data = {
        symbol: df.to_dict(orient="records") for symbol, df in filtered_stocks.items()
    }

    return {"filtered_stocks": list(filtered_stocks.keys()), "details": response_data}
