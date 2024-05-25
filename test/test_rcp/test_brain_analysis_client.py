import pytest
import os
from PIL import Image
import base64
from core.config import config
import json
from core.rcp_client import rpcClient


def test_brain_analysis_client():
    ans = [3,2,0,1,1,1,0,0,2,1,1,0,0,2,1]
    dictionary = {
        0: "Аномалий не обнаружено",
        1: "Обнаружена менингиома, советуем обратиться к специалисту",
        2: "Обнаружена глинома, советуем обратиться к специалисту",
        3: "Обнаружена аномалия в гипофизе, советуем обратиться к специалисту"
                  }
    for i in range(0,20):
        i=i%15
        file_path = ""
        if i<10:
            file_path = f"/home/sasha/health_checker/HealthCheck/test/test_rcp/test_images/brain_test_images/{i}.png"
        else:
            file_path = f"/home/sasha/health_checker/HealthCheck/test/test_rcp/test_images/brain_test_images/{i}.jpeg"
        with open(file_path, 'rb') as file:
            photo_binary_data = file.read()
            encoded_data = base64.b64encode(photo_binary_data)
            assert json.loads(rpcClient.call(encoded_data, config.brain_analysis_queue)) == dictionary[ans[i]]

