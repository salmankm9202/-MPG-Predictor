import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import joblib
import os
import numpy as np


class MPGModelTrainer:
    def __init__(self, data_path="data/auto-mpg-cleaned.csv"):
        self.data_path = data_path
        os.makedirs("models", exist_ok=True)

    def train_model(self):
        """Train Linear Regression model."""
        df = pd.read_csv(self.data_path)
        X = df[['cylinders', 'horsepower', 'weight', 'model_year']]
        y = df['mpg']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = LinearRegression()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        print(f"R² Score: {r2_score(y_test, y_pred):.2f}")

        # Universal RMSE calculation that works in all versions
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        print(f"RMSE: {rmse:.2f}")

        joblib.dump(model, "models/mpg_model.pkl")
        print("Model saved to models/mpg_model.pkl")
        return model


if __name__ == "__main__":
    trainer = MPGModelTrainer()
    trainer.train_model()