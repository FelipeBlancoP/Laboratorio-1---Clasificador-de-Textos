import numpy as np
import pandas as pd

def classify_days(df):
    daily_avg = df.groupby(df["Date"])["CO(GT)"].mean().reset_index()
    daily_avg.columns = ["Date", "CO_daily_avg"]

    daily_avg["day_type"] = np.where(
        daily_avg["CO_daily_avg"] > 7, "Contaminado", "Normal"
    )

    return daily_avg