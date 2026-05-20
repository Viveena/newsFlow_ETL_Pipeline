CREATE DATABASE IF NOT EXISTS news_db;

USE news_db;

CREATE TABLE IF NOT EXISTS news_articles (

    id INT AUTO_INCREMENT PRIMARY KEY,

    title TEXT,

    source VARCHAR(255),

    publishedAt DATETIME,

    clean_title TEXT,

    title_length INT
);