import pandas as pd
from sklearn.ensemble import IsolationForest


class DataPreprocessor:
    def __init__(self):
        self.anomaly_detector = IsolationForest(contamination=0.05)

    def clean_data(self, df):
        # Handle missing values
        df['horsepower'] = pd.to_numeric(df['horsepower'], errors='coerce')
        df = df.dropna()

        # Feature engineering
        df['power_to_weight'] = df['horsepower'] / df['weight']
        df['age'] = 2024 - df['model_year']

        # Anomaly detection
        df['anomaly'] = self.anomaly_detector.fit_predict(df[['mpg', 'weight', 'horsepower']])
        return df[df['anomaly'] == 1]  # Keep only normal records