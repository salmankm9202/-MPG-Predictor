from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV
import joblib
import pandas as pd
from src.data_loader import DataLoader
from src.preprocess import DataPreprocessor


def train_model():
    # Load and preprocess data
    df = DataLoader().load_data()
    clean_df = DataPreprocessor().clean_data(df)

    # Prepare features
    X = clean_df[['cylinders', 'horsepower', 'weight', 'model_year']]
    y = clean_df['mpg']

    # Model training with tuning
    model = XGBRegressor(objective='reg:squarederror')
    param_grid = {'max_depth': [3, 5], 'learning_rate': [0.01, 0.1]}

    best_model = GridSearchCV(model, param_grid, cv=5).fit(X, y)
    joblib.dump(best_model, "models/mpg_model.pkl")
    print(f"Best model R²: {best_model.best_score_:.2f}")


if __name__ == "__main__":
    train_model()