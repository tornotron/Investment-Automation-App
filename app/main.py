from fastapi import FastAPI
from app.api.v1.endpoints import user, portfolio, trade

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(portfolio.router, prefix="/portfolios", tags=["portfolios"])
app.include_router(trade.router, prefix="/trades", tags=["trades"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Investment Automation App"}

@app.get("/fetch")
async def fetch():
    return {"message": "select data source"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)