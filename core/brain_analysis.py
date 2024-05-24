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
from torchvision import models
from torch import nn

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=config.host))

channel = connection.channel()
channel.queue_declare(queue=config.brain_analysis_queue)


class AdvancedMRI_Classifier(nn.Module):
    def __init__(self, num_classes):
        super(AdvancedMRI_Classifier, self).__init__()
        
        self.conv_block1 = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Dropout(0.25)
        )
        
        self.conv_block2 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Dropout(0.25)
        )
        
        self.fc_block = nn.Sequential(
            nn.Linear(64 * 56 * 56, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        )

    def forward(self, x):
        x = self.conv_block1(x)
        x = self.conv_block2(x)
        x = x.view(x.size(0), -1)
        x = self.fc_block(x)
        return x
model = AdvancedMRI_Classifier(4)
model.load_state_dict(torch.load('ml/model_28', map_location=torch.device('cpu')))
model.eval()


def brain_analysis(image):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    data_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
    image = data_transforms(image)
    image = image.unsqueeze(0)
    ans = ""
    if torch.cuda.is_available():
        images=Variable(images.cuda())
    with torch.no_grad():
        output = model(image)
        _,prediction=torch.max(output.data,1)
        if prediction == torch.tensor([0]):
            ans = "Обнаружена менингиома, советуем обратиться к специалисту"
        elif prediction == torch.tensor([1]):
            ans = "Обнаружена глинома, советуем обратиться к специалисту"
        elif prediction == torch.tensor([2]):
            ans = "Обнаружена аномалия в гипофизе, советуем обратиться к специалисту"
        else:
            ans = "Аномалий не обнаружено"
    return ans

def on_request(ch, method, props, body):
    body = body[2:-1]
    decoded_data = base64.b64decode(body)
    image = Image.open(io.BytesIO(decoded_data))
    response = json.dumps(brain_analysis(image))
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


#1 менингиома
#2 глинома
#3 гипофиз