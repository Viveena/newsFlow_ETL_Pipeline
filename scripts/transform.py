import pandas as pd
import redis
import json
import os

REDIS_HOST = "localhost"
if os.path.exists("/opt/airflow"):
    REDIS_HOST = "newsflow_redis"

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=6379,
    decode_responses=True
)

def transform_data():

    cached_news = redis_client.get("latest_news")

    if cached_news:
        print("Reading data from Redis")

        news_data = json.loads(cached_news)

        df = pd.DataFrame(news_data)

    else:
        print("Redis cache miss. Reading CSV")

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

    output_path = "data/news_transformed.csv"

    if os.path.exists("/opt/airflow"):
        output_path = "/opt/airflow/data/news_transformed.csv"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df.to_csv(output_path, index=False)


    print("Stored transformed data in Redis")

    print("\nTransformation Complete")
    print(df.head())


if __name__ == "__main__":
    transform_data()