import json
import pika
import time
import asyncio
from PIL import Image
import io
import base64
import cv2
import numpy as np
import tensorflow as tf
import os
import numpy
from memory_profiler import profile

model = tf.keras.models.load_model("/home/sasha/health_checker/HealthCheck/core/ml/x_ray_effnet_b1.h5")

@profile
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


def test_memory_used():
    file_path = f"/home/sasha/health_checker/HealthCheck/test/test_model/test_images/xray1.png"
    with open(file_path, 'rb') as file:
        photo = file.read()
        xray_analysis(photo)


if __name__ == "__main__":
    test_memory_used()