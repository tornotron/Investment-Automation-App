import pandas as pd


def parse_ticker_file(file_path: str, file_type: str) -> pd.DataFrame:
    if file_type == "csv":
        df = pd.read_csv(file_path, skiprows=4)
    elif file_type == "excel":
        df = pd.read_excel(file_path, skiprows=4)
    else:
        raise ValueError("Unsupported file type")

    df.columns = ["Ticker", "Name", "Exchange", "Category Name", "Country"]
    return df
