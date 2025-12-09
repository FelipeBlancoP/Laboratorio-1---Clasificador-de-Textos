from data_prep import process_csv
from exploratory import run_eda
from models.model_1 import run_model_1

def main():
    df = process_csv(
        input_path="data/raw/AirQualityUCI.csv",
        output_path="data/processed/AirQuality_processed.csv"
    )

    run_eda(df)

    run_model_1(df)

if __name__ == "__main__":
    main()