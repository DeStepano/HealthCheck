import json
import pika
import time
import asyncio
import pandas as pd
import torch
from xgboost import XGBClassifier
import joblib
from memory_profiler import profile


path = "your project path"
model = joblib.load(f"{path}/HealthCheck/core/ml/Diabetes_model-2.pkl")


@profile
def diabetes_analysis(data):
    features = ['gender', 'age', 'hypertension', 'heart_disease', 'smoking_history', 'bmi', 'HbA1c_level', 'blood_glucose_level']
    custom_df = pd.DataFrame(data, columns=features)
    y_pred = model.predict(custom_df)
    answer = ""
    if y_pred[0] == 1:
        answer = "У вас есть подозрение на диабет"
    else:
        answer = "Аномалий не обнаружено"
    return answer


def test_memory_usage():
    data = [[0, 80.0, 0, 1, 4, 25.19, 6.6, 140]]
    diabetes_analysis(data)


if __name__ == "__main__":
    test_memory_usage()
