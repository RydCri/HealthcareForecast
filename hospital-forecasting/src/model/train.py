import pandas as pd
import joblib
from prophet import Prophet
from utils.paths import CLEANED_ADMISSIONS_PATH, MODELS_DIR
import pickle
import os
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def train_admissions_model():
    df = pd.read_csv(CLEANED_ADMISSIONS_PATH)
    df = df.rename(columns={"admission_date": "ds", "admissions": "y"})

    model = Prophet()
    model.fit(df)

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODELS_DIR / "admissions_forecast_model.pkl")
    print("✅ Model trained and saved.")


def train_model():
    # Trains a regression model on admissions data and saves it to disk.
    # Expects a CSV at /opt/airflow/include/admissions_features.csv

    data_path = "/opt/airflow/include/admissions_features.csv"
    output_path = "/opt/airflow/include/model.pkl"

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Training data not found at {data_path}")

    df = pd.read_csv(data_path)

    if "target" not in df.columns:
        raise ValueError("Expected a 'target' column in training data.")

    # Split features and target
    X = df.drop(columns=["target"])
    y = df["target"]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model (Linear Regression here for simplicity)
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Save model
    with open(output_path, "wb") as f:
        pickle.dump(model, f)

    print(f"Model trained and saved to {output_path}")
