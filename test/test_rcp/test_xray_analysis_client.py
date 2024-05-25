import pytest
import os
from PIL import Image
import base64
from core.config import config
import json
from core.rcp_client import rpcClient



def test_xray_analysis_client():
    ans = [0,0,1,0,1,0,0,1,0,1]
    dictionary={0:"Пневмонии не обнаружено", 1: "Обнаружена аномалия! Вам следует обратиться к специалисту."}
    for i in range(1,50):
        i=i%10
        file_path = ""
        if i<5:
            file_path = f"/home/sasha/health_checker/HealthCheck/test/test_rcp/test_images/xray_test_image/{i}.png"
        else:
            file_path = f"/home/sasha/health_checker/HealthCheck/test/test_rcp/test_images/xray_test_image/{i}.jpg"
        with open(file_path, 'rb') as file:
            photo_binary_data = file.read()
            encoded_data = base64.b64encode(photo_binary_data)
            assert json.loads(rpcClient.call(encoded_data, config.xray_queue)) == dictionary[ans[i]]