import pandas as pd
from sqlalchemy import create_engine
import redis
import json
import os

# Auto-detect environment
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_DB = "news_db"

MYSQL_HOST = "localhost"
MYSQL_PORT = "3308"

REDIS_HOST = "localhost"

# If running inside Airflow container
if os.path.exists("/opt/airflow"):
    MYSQL_HOST = "newsflow_mysql"
    MYSQL_PORT = "3306"

    REDIS_HOST = "newsflow_redis"

# Redis Connection
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=6379,
    decode_responses=True
)


def load_to_mysql():

    cached_data = redis_client.get("transformed_news")

    if cached_data:
        print("Loading data from Redis")

        df = pd.DataFrame(json.loads(cached_data))

    else:
        print("Redis cache miss. Reading CSV")

        csv_path = "data/news_transformed.csv"

        if os.path.exists("/opt/airflow"):
            csv_path = "/opt/airflow/data/news_transformed.csv"

        df = pd.read_csv(csv_path)

    # MySQL Connection
    engine = create_engine(
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )

    # Load Data
    df.to_sql(
        name="news_articles",
        con=engine,
        if_exists="append",
        index=False
    )

    print("Data Loaded Successfully into MySQL")

    # Clear Redis Cache
    redis_client.delete("latest_news")
    redis_client.delete("transformed_news")

    print("Redis cache cleared")


if __name__ == "__main__":
    load_to_mysql()