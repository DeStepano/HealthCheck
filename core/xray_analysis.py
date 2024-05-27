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

model = tf.keras.models.load_model("ml/x_ray_effnet_b1.h5")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=config.rcp_host))

channel = connection.channel()

channel.queue_declare(queue=config.xray_queue)

def xray_analysis(image):
    image_size = 128
    uploaded = image
    img_np = np.frombuffer(uploaded, np.uint8)
    uploaded_img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    resized_image = cv2.resize(uploaded_img, (image_size, image_size))
    predict_in = []
    predict_in.append(resized_image)
    predict_in = np.array(predict_in)  
    prediction = model.predict(predict_in)
    return prediction[0][0]

def on_request(ch, method, props, body):
    body = body[2:-1]
    decoded_data = base64.b64decode(body)
    image = decoded_data
    res = xray_analysis(image)
    response = ""
    if res >= 0.5:
        response = json.dumps("Обнаружена аномалия! Вам следует обратиться к специалисту.")
    else:
        response = json.dumps("Пневмонии не обнаружено")

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