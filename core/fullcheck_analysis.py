import json
import pika
import time
import asyncio
from config import config
import torch
import torch.nn as nn
from torch import load
from torch.optim import Adam


connection_fullcheck = pika.BlockingConnection(
    pika.ConnectionParameters(host=config.rcp_host))
channel_fullcheck = connection_fullcheck.channel()
channel_fullcheck.queue_declare(queue=config.fullcheck_queue)


class CustomModel(nn.Module):
    def __init__(self):
        super(CustomModel, self).__init__()
        self.fc1 = nn.Linear(989, 989)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(989, 989)
        self.relu = nn.ReLU()
        self.fc3 = nn.Linear(989, 256)
        self.relu = nn.ReLU()
        self.fc4 = nn.Linear(256, 49)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        x = self.relu(x)
        x = self.fc4(x)
        x = self.sigmoid(x)
        return x


model_fullcheck = CustomModel()
model_fullcheck = load('ml/full_ml.pth')
model_fullcheck.eval()


diseases = {
    0: "Обострение ХОБЛ / инфекция",
    1: "Острые дистонические реакции",
    2: "Острый ларингит",
    3: "Острый средний отит",
    4: "Острый отек легких",
    5: "Острый риносинусит",
    6: "Аллергический синусит",
    7: "Анафилаксия",
    8: "Анемия",
    9: "Фибрилляция предсердий",
    10: "Синдром Боэрхаве",
    11: "Бронхоэктатическая болезнь",
    12: "Бронхиолит",
    13: "Бронхит",
    14: "Бронхоспазм / обострение астмы",
    15: "Болезнь Шагаса",
    16: "Хронический риносинусит",
    17: "Кластерная головная боль",
    18: "Крупозный ларингит",
    19: "Эбола",
    20: "Эпиглоттит",
    21: "ГЭРБ",
    22: "Синдром Гийена-Барре",
    23: "ВИЧ (первичная инфекция)",
    24: "Грипп",
    25: "Паховая грыжа",
    26: "Спазм гортани",
    27: "Локализованный отек",
    28: "Миастения гравис",
    29: "Миокардит",
    30: "ПНЖТ",
    31: "Новообразование поджелудочной железы",
    32: "Паническая атака",
    33: "Перикардит",
    34: "Пневмония",
    35: "Вероятная НСТ / ИМ",
    36: "Легочная эмболия",
    37: "Легочное новообразование",
    38: "СКВ",
    39: "Саркоидоз",
    40: "Скомброидное отравление",
    41: "Самопроизвольный пневмоторакс",
    42: "Самопроизвольный перелом ребра",
    43: "Стабильная стенокардия",
    44: "Туберкулез",
    45: "ОРВИ",
    46: "Нестабильная стенокардия",
    47: "Вирусный фарингит",
    48: "Коклюш"
    }


def fullcheck_analysis(data):
    out = model_fullcheck.forward(torch.tensor(data).float()).detach().numpy()
    trashhold = 0.10
    out = (out>=trashhold).astype(int)
    ans = "Под данные симптомы больше всего подпадают данные заболевания: \n"
    f = True
    for i in range(49):
        if out[i] >0:
            ans+=diseases[i] +' ' + str(round(out[i], 3)) + '\n'
            f=False
    if f:
        ans = "Заболевание не определено"
    return ans


def on_request(ch, method, props, body):
    body = json.loads(body)
    response = json.dumps(fullcheck_analysis(body))
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel_fullcheck.basic_qos(prefetch_count=1)
channel_fullcheck.basic_consume(queue=config.fullcheck_queue, on_message_callback=on_request)
print(" [x] Awaiting RPC requests")
channel_fullcheck.start_consuming()