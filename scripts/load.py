import pandas as pd
from sqlalchemy import create_engine

MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_HOST = "newsflow_mysql"
MYSQL_PORT = "3306"
MYSQL_DB = "news_db"

def load_to_mysql():

    # Read transformed CSV
    df = pd.read_csv("/opt/airflow/data/news_transformed.csv")

    # MySQL connection
    engine = create_engine(
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )

    # Insert data into table
    df.to_sql(
        name="news_articles",
        con=engine,
        if_exists="append",
        index=False
    )

    print("Data Loaded Successfully into MySQL")


if __name__ == "__main__":
    load_to_mysql()