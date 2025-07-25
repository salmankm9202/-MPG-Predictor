from fastapi import FastAPI
import joblib
import pandas as pd
from src.database import PredictionLogger

app = FastAPI()
model = joblib.load("../models/mpg_model.pkl")
logger = PredictionLogger()

@app.post("/predict")
async def predict(cylinders: float, horsepower: float,
                 weight: float, model_year: float):
    features = {
        'cylinders': cylinders,
        'horsepower': horsepower,
        'weight': weight,
        'model_year': model_year
    }
    prediction = model.predict(pd.DataFrame([features]))[0]
    logger.log_prediction(features, prediction)
    return {"mpg_prediction": prediction}