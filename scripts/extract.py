
import requests
import pandas as pd
import os

API_KEY = "4f226ed902994f6f8a2b5172159f735d"

def extract_news():

    url = f"https://newsapi.org/v2/top-headlines?category=technology&language=en&apiKey={API_KEY}"

    response = requests.get(url)

    data = response.json()

    articles = data["articles"]

    news_list = []

    for article in articles:

        news_list.append({
            "title": article["title"],
            "source": article["source"]["name"],
            "publishedAt": article["publishedAt"]
        })

    df = pd.DataFrame(news_list)

    DATA_PATH = "data/news_data.csv"

    if os.path.exists("/opt/airflow"):
        DATA_PATH = "/opt/airflow/data/news_data.csv"

    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

    df.to_csv(DATA_PATH, index=False)

    print("News Extracted Successfully")
    print(df.head())



if __name__ == "__main__":
    extract_news()