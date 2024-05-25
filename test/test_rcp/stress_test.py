import pytest
import os
from PIL import Image
import base64
from core.config import config
import json
from core.rcp_client import rpcClient
import time

def test_rcp():
    ans_brain = [3,2,0,1,1,1,0,0,2,1,1,0,0,2,1]
    dictionary_brain = {
        0: "Аномалий не обнаружено",
        1: "Обнаружена менингиома, советуем обратиться к специалисту",
        2: "Обнаружена глинома, советуем обратиться к специалисту",
        3: "Обнаружена аномалия в гипофизе, советуем обратиться к специалисту"
                  }
    ans_xray = [0, 0, 1, 0, 1, 0, 0, 1, 0, 1]
    dictionary_xray = {
        0: "Пневмонии не обнаружено",
        1: "Обнаружена аномалия! Вам следует обратиться к специалисту."
                    }
    for i in range(0,100):
        i_brain =i % 15
        file_path_brain = ""
        if i_brain < 10:
            file_path_brain = f"/home/sasha/health_checker/HealthCheck/test/test_rcp/test_images/brain_test_images/{i_brain}.png"
        else:
            file_path_brain = f"/home/sasha/health_checker/HealthCheck/test/test_rcp/test_images/brain_test_images/{i_brain}.jpeg"
        with open(file_path_brain, 'rb') as file:
            photo_binary_data = file.read()
            encoded_data = base64.b64encode(photo_binary_data)
            assert json.loads(rpcClient.call(encoded_data, config.brain_analysis_queue)) == dictionary_brain[ans_brain[i_brain]]

        i_xray = i % 10
        file_path_xray = ""
        if i_xray < 5:
            file_path_xray = f"/home/sasha/health_checker/HealthCheck/test/test_rcp/test_images/xray_test_image/{i_xray}.png"
        else:
            file_path_xray = f"/home/sasha/health_checker/HealthCheck/test/test_rcp/test_images/xray_test_image/{i_xray}.jpg"
        with open(file_path_xray, 'rb') as file:
            photo_binary_data = file.read()
            encoded_data = base64.b64encode(photo_binary_data)
            assert json.loads(rpcClient.call(encoded_data, config.xray_queue)) == dictionary_xray[ans_xray[i_xray]]