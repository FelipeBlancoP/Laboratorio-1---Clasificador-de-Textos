import pandas as pd
import numpy as np

def process_csv(input_path, output_path):
    df = pd.read_csv(input_path, sep=";", decimal=",")
    df = df.iloc[:, :-1]

    #Preparación de datos
    #Eliminar cualquier fila que contenga un -200
    df = df[(df != -200).all(axis=1)]

    #Convertir fecha y hora
    df["DateTime"] = pd.to_datetime(
        df["Date"] + " " + df["Time"],
        format="%d/%m/%Y %H.%M.%S"
    )

    df["year"] = df["DateTime"].dt.year
    df["month"] = df["DateTime"].dt.month
    df["day"] = df["DateTime"].dt.day
    df["hour"] = df["DateTime"].dt.hour

    df["weekday"] = df["DateTime"].dt.day_name()
    df["weekday_num"] = df["DateTime"].dt.weekday
    df["is_weekend"] = df["weekday_num"].isin([5, 6]).astype(int)

    #Reordenar columnas
    cols_time = ["DateTime", "Date", "Time", "year", "month", "day", "hour", "weekday", "weekday_num", "is_weekend"]
    other_cols = [c for c in df.columns if c not in cols_time]

    df = df[cols_time + other_cols]
    df = df.dropna(thresh=5)

    #Exportar CSV
    df.to_csv(output_path, index=False)
    return df
