import json
import pika
import time
import asyncio
import pandas as pd
import torch
from xgboost import XGBClassifier
import joblib


model = joblib.load('/home/sasha/health_checker/HealthCheck/core/ml/Diabetes_model-2.pkl')


def test_loading():
    assert isinstance(model, XGBClassifier)


def test_first_sample():
    data = [[0, 80.0, 0, 1, 4, 25.19, 6.6, 140]]
    features = ['gender', 'age', 'hypertension', 'heart_disease', 'smoking_history', 'bmi', 'HbA1c_level', 'blood_glucose_level']
    custom_df = pd.DataFrame(data, columns=features)
    y_pred = model.predict(custom_df)
    assert y_pred == [0]