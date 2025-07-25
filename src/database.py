import sqlite3
from datetime import datetime


class PredictionLogger:
    def __init__(self):
        self.conn = sqlite3.connect('predictions.db')
        self._init_db()

    def _init_db(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY,
                username TEXT,
                cylinders REAL,
                horsepower REAL,
                weight REAL,
                model_year REAL,
                prediction REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

    def log_prediction(self, username, features, prediction):
        self.conn.execute('''
            INSERT INTO predictions 
            (username, cylinders, horsepower, weight, model_year, prediction)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            username,
            features['cylinders'],
            features['horsepower'],
            features['weight'],
            features['model_year'],
            prediction
        ))
        self.conn.commit()