import json
import joblib
import pandas as pd

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor

# ------------------ CONFIG ------------------
MODEL_NAME = "Random Forest (150, depth=15, Stratified)"
DATA_PATH = "dataset/winequality-red.csv"

# ------------------ LOAD DATA ------------------
data = pd.read_csv(DATA_PATH, sep=";")

X = data.drop("quality", axis=1)
y = data["quality"]

# Create bins for stratified regression split
y_bins = pd.qcut(y, q=5, labels=False, duplicates="drop")

# ------------------ TRAIN-TEST SPLIT ------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    stratify=y_bins,
    random_state=42
)

# ------------------ MODEL ------------------
model = RandomForestRegressor(
    n_estimators=150,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# ------------------ EVALUATION ------------------
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# ------------------ SAVE MODEL (ROOT for GitHub Artifact) ------------------
joblib.dump(model, "model.pkl")

# ------------------ SAVE METRICS (For CI Gate) ------------------
metrics = {
    "model_name": MODEL_NAME,
    "r2": float(r2),
    "mse": float(mse)
}

with open("metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

# ------------------ LOGS ------------------
print("\n===== RANDOM FOREST STRATIFIED RUN =====")
print(f"Model: {MODEL_NAME}")
print(f"R2 Score: {r2}")
print(f"MSE: {mse}")
print("Model saved as model.pkl")
print("Metrics saved as metrics.json")
