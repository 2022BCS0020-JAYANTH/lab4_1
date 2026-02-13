import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os

MODEL_PATH = "model.pkl" 

if not os.path.exists(MODEL_PATH):
    MODEL_PATH = "app/artifacts/model.pkl"

model = joblib.load(MODEL_PATH)

app = FastAPI()

class WineFeatures(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float

@app.get("/")
def home():
    return {
        "status": "Success",
        "message": "Wine Quality Prediction API",
        "developer": "K. Jayanth"
    }

@app.post("/predict")
def predict(features: WineFeatures):
    X = np.array([[
        features.fixed_acidity, features.volatile_acidity, features.citric_acid,
        features.residual_sugar, features.chlorides, features.free_sulfur_dioxide,
        features.total_sulfur_dioxide, features.density, features.pH,
        features.sulphates, features.alcohol
    ]])
    
    prediction = model.predict(X)[0]
    wine_quality = int(round(prediction))

    return {
        "name": "K. Jayanth",
        "roll_no": "2022BCS0020",
        "wine_quality": wine_quality
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
