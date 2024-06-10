from fastapi import FastAPI
from app.api.v1.endpoints import (
    assets,
    auth,
    user,
    portfolio,
    trade,
    ticker,
)
import logging

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(portfolio.router, prefix="/portfolios", tags=["portfolios"])
app.include_router(trade.router, prefix="/trades", tags=["trades"])
app.include_router(assets.router, prefix="/assets", tags=["assets"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(ticker.router, prefix="/tickers", tags=["tickers"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Investment Automation App"}


@app.get("/fetch")
async def fetch():
    return {"message": "select data source"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
