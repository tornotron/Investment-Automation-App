from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "first fastapi"}

@app.get("/fetch")
async def fetch():
    return {"message": "select data source"}