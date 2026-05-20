import pandas as pd

def transform_data():

    df = pd.read_csv("/opt/airflow/data/news_data.csv")

    print("Original Data")
    print(df.head())

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # Remove null values
    df.dropna(inplace=True)

    # Convert titles to lowercase
    df["clean_title"] = df["title"].str.lower()

    # Calculate title length
    df["title_length"] = df["title"].apply(len)

    # Convert date column
    df["publishedAt"] = pd.to_datetime(df["publishedAt"])

    # Save transformed data
    df.to_csv("/opt/airflow/data/news_transformed.csv", index=False)

    print("\nTransformation Complete")
    print(df.head())


if __name__ == "__main__":
    transform_data()