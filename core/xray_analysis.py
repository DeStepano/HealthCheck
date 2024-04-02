import json
import pika
import time
import asyncio
from PIL import Image
import io
import base64
from config import config
import cv2
import numpy as np
import tensorflow as tf
import os
import numpy

# model = tf.keras.models.load_model("ml/effnet.keras")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=config.host))

channel = connection.channel()

channel.queue_declare(queue=config.xray_queue)

def xray_analysis(image):
    # predict_in = []
    # image_size = 256
    # img = cv2.imread(os.path.join("путь в папку","название файла (фото)"))
    # img = cv2.resize(img,(image_size, image_size))
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # predict_in.append(img)
    # predict_in.append(img)
    # prediction = model.predict(predict_in)
    # result = prediction[0]
    time.sleep(3)
    response = "Обнаружена аномалия. Рекомендуем обратиться к специалисту"
    return response

def on_request(ch, method, props, body):
    body = body[2:-1]
    decoded_data = base64.b64decode(body)
    image = Image.open(io.BytesIO(decoded_data))
    response = json.dumps(xray_analysis(image))
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=config.xray_queue, on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()