import json
import pika
import time
import asyncio
from PIL import Image
import io
import base64
from config import config
import torch
import torchvision.transforms as transforms
from torch.autograd import Variable

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=config.host))

channel = connection.channel()

channel.queue_declare(queue=config.brain_analysis_queue)

model = torch.load('ml/best_model.model', map_location=torch.device('cpu'))

def brain_analysis(image):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    data_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
    image = data_transforms(image)
    image = image.unsqueeze(0)
    model.eval()
    if torch.cuda.is_available():
            images=Variable(images.cuda())
    with torch.no_grad():
        output = model(image)
        print(output.data)
        _,prediction=torch.max(output.data,1)
        print(prediction)
    return 1

def on_request(ch, method, props, body):
    body = body[2:-1]
    decoded_data = base64.b64decode(body)
    image = Image.open(io.BytesIO(decoded_data))
    res = brain_analysis(image)
    response = ""
    if res>0.5:
        response = json.dumps("Обнаружена аномалия")
    else:
        response = json.dumps("Анломалий не обнаружено")
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=config.brain_analysis_queue, on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()