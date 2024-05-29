from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import crud, models, schemas
from app.api.v1.dependencies import get_db

router = APIRouter()


@router.post("/upload_tickers/{provider}", response_model=schemas.Message)
def upload_tickers(
    provider: str, file: UploadFile = File(...), db: Session = Depends(get_db)
):
    file_type = file.filename.split(".")[-1]
    if file_type not in ["csv", "xlsx"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # Save the uploaded file to disk
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    # Parse the file
    tickers_df = parse_ticker_file(file_path, file_type)

    # Clear existing tickers for the provider
    crud.delete_tickers_by_provider(db, provider)

    # Insert new tickers
    crud.insert_tickers(db, tickers_df, provider)

    return {"message": "Tickers uploaded successfully"}


@router.get("/tickers/{provider}", response_model=List[schemas.Ticker])
def get_tickers(provider: str, db: Session = Depends(get_db)):
    return db.query(models.Ticker).filter(models.Ticker.provider == provider).all()
