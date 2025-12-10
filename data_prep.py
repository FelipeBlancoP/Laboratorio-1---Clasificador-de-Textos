import pandas as pd
import numpy as np

def process_csv(input_path, output_path):
    df = pd.read_csv(input_path, sep=";", decimal=",")
    df = df.iloc[:, :-1]

    df.replace(-200, np.nan, inplace=True)

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    df["DateTime"] = pd.to_datetime(
        df["Date"] + " " + df["Time"],
        format="%d/%m/%Y %H.%M.%S",
        errors="coerce"
    )

    df["year"] = df["DateTime"].dt.year
    df["month"] = df["DateTime"].dt.month
    df["day"] = df["DateTime"].dt.day
    df["hour"] = df["DateTime"].dt.hour
    df["weekday"] = df["DateTime"].dt.day_name()
    df["weekday_num"] = df["DateTime"].dt.weekday
    df["is_weekend"] = df["weekday_num"].isin([5, 6]).astype(int)

    cols_time = [
        "DateTime", "Date", "Time", "year", "month", "day", "hour",
        "weekday", "weekday_num", "is_weekend"
    ]
    other_cols = [c for c in df.columns if c not in cols_time]
    df = df[cols_time + other_cols]

    df = df.dropna(axis=1, how="all")
    df = df.dropna(thresh=5)

    df.to_csv(output_path, index=False)
    return df
