import json
import pika
import time
import asyncio
import pandas as pd
from config import config
import torch
from xgboost import XGBClassifier
import joblib
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=config.rcp_host))

channel = connection.channel()

channel.queue_declare(queue=config.first_check_queue)


model = joblib.load('ml/Diabetes_model-2.pkl')

def first_check_analysis(data):
    features = ['gender', 'age', 'hypertension', 'heart_disease', 'smoking_history', 'bmi', 'HbA1c_level', 'blood_glucose_level']
    custom_df = pd.DataFrame(data, columns=features)
    y_pred = model.predict(custom_df)
    answer = ""
    if y_pred[0] == 1:
        answer = "У вас есть подозрение на диабет"
    else:
        answer = "Аномалий не обнаружено"
    return answer


def on_request(ch, method, props, body):
    body = json.loads(body)
    response = json.dumps(first_check_analysis(body))
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=config.first_check_queue, on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()