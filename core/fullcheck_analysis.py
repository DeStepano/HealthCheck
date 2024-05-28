import json
import pika
import time
import asyncio
from config import config
import torch
import torch.nn as nn

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=config.rcp_host))
channel = connection.channel()
channel.queue_declare(queue=config.fullcheck_queue)

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

model = CustomModel()
criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters())
model = torch.load('ml/full_ml.pth')
model.eval()

def fullcheck_analysis(data):
    # answer = model.predict(data)
    answer="12345"
    return answer


def on_request(ch, method, props, body):
    body = json.loads(body)
    print("получено")
    response = json.dumps(fullcheck_analysis(body))
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=config.fullcheck_queue, on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()