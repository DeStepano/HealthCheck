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
import pytest


path = "your project path"
model = tf.keras.models.load_model(f"{path}/HealthCheck/core/ml/x_ray_effnet_b1.h5")


def test_loading():
    assert isinstance(model, tf.keras.Model)


def test_first_sample():
    file_path = f"{path}/HealthCheck/test/test_model/test_images/xray1.png"
    with open(file_path, 'rb') as file:
        photo = file.read()
        image_size = 128
        uploaded = photo
        img_np = np.frombuffer(uploaded, np.uint8)
        uploaded_img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
        resized_image = cv2.resize(uploaded_img, (image_size, image_size))
        predict_in = []
        predict_in.append(resized_image)
        predict_in = np.array(predict_in)  
        prediction = model.predict(predict_in)
        assert prediction[0][0] <= 0.5


def test_inference_batch():
    ans = [0,0,1,0,1,0,0,1,0,1]
    for i in range(1,10):
        file_path = ""
        if i<5:
            file_path = f"{path}/HealthCheck/test/test_model/test_images/xray_test_images/{i}.png"
        else:
            file_path = f"/{path}/HealthCheck/test/test_model/test_images/xray_test_images/{i}.jpg"
        with open(file_path, 'rb') as file:
            photo = file.read()
            image_size = 128
            uploaded = photo
            img_np = np.frombuffer(uploaded, np.uint8)
            uploaded_img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
            resized_image = cv2.resize(uploaded_img, (image_size, image_size))
            predict_in = []
            predict_in.append(resized_image)
            predict_in = np.array(predict_in)  
            prediction = model.predict(predict_in)
            if ans[i]:
                assert prediction[0][0]>=0.5
            else:
                assert prediction[0][0]<0.5
