import pandas as pd
from sklearn.metrics import mean_absolute_error

def evaluate_model_performance():
    # Evaluates the model's forecast accuracy using MAE.

    y_true = pd.read_csv("/opt/airflow/include/actuals.csv")["value"]
    y_pred = pd.read_csv("/opt/airflow/include/forecast.csv")["value"]

    mae = mean_absolute_error(y_true, y_pred)
    print(f"Model MAE: {mae}")
    return mae
