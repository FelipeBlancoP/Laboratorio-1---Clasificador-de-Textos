from data_prep import process_csv

def main():
    df = process_csv(
        input_path="data/raw/AirQualityUCI.csv",
        output_path="data/processed/AirQuality_processed.csv"
    )

if __name__ == "__main__":
    main()