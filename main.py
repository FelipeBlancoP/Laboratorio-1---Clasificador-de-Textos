from data_prep import process_csv
from exploratory import run_eda

def main():
    df = process_csv(
        input_path="data/raw/AirQualityUCI.csv",
        output_path="data/processed/AirQuality_processed.csv"
    )

    run_eda(df)

if __name__ == "__main__":
    main()