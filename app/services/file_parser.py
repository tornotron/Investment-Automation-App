import pandas as pd


def parse_ticker_file(file_path: str, file_type: str) -> pd.DataFrame:
    if file_type == "csv":
        # Read the CSV file without header
        df = pd.read_csv(file_path, header=None)

        # Extract the first row to use as column names
        new_column_names = df.iloc[0].tolist()

        # Set the new column names
        df.columns = new_column_names

        # Drop the first row which was used as column names
        df = df.drop(df.index[0])
    elif file_type == "xlsx":
        # Read the Excel file without header
        df = pd.read_excel(file_path, header=None, dtype=str)

        # Extract the first row to use as column names
        new_column_names = df.iloc[0].tolist()

        # Set the new column names
        df.columns = new_column_names

        # Drop the first row which was used as column names
        df = df.drop(df.index[0]).reset_index(drop=True)
    else:
        raise ValueError("Unsupported file type")

    # Drop rows where all values are null
    df = df.dropna(axis=0, how="all")

    # Convert all data types to string
    df = df.astype(str)

    return df
