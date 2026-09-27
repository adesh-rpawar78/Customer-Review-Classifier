-- Reference schema. app.py calls init_db() on startup, which creates these
-- tables automatically if they don't exist — running this file by hand is
-- optional, but useful if you want to inspect or set up the DB manually.

CREATE DATABASE IF NOT EXISTS review_classifier;
USE review_classifier;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    review_text TEXT NOT NULL,
    prediction TINYINT NOT NULL,
    sentiment_pos FLOAT,
    sentiment_neu FLOAT,
    sentiment_neg FLOAT,
    sentiment_compound FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
