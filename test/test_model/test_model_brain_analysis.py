import json
import pika
import time
import asyncio
from PIL import Image
import io
import base64
import torch
import torchvision.transforms as transforms
from torch.autograd import Variable
from torchvision import models
from torch import nn
import io


path = "your project path"


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
model.load_state_dict(torch.load(f"{path}/HealthCheck/core/ml/model_28", map_location=torch.device('cpu')))
model.eval()


def test_loading():
    assert isinstance(model, nn.Module)


def test_first_sample():
    file_path = f"/home/sasha/health_checker/HealthCheck/test/test_model/test_images/brain1.png"
    with open(file_path, 'rb') as file:
        photo = file.read()
        image = Image.open(io.BytesIO(photo))
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
            print(prediction)
            assert prediction == torch.tensor([3])


def test_inference_batch():
    ans = [2,1,3,0,0,0,3,3,1,0,0,3,3,1,0]
    for i in range(0,15):
        i=i%15
        file_path = ""
        if i<10:
            file_path = f"/home/sasha/health_checker/HealthCheck/test/test_model/test_images/brain_test_images/{i}.png"
        else:
            file_path = f"/home/sasha/health_checker/HealthCheck/test/test_model/test_images/brain_test_images/{i}.jpeg"
        with open(file_path, 'rb') as file:
            photo = file.read()
            image = Image.open(io.BytesIO(photo))
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            data_transforms = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
            image = data_transforms(image)
            image = image.unsqueeze(0)
            if torch.cuda.is_available():
                images=Variable(images.cuda())
            with torch.no_grad():
                output = model(image)
                _,prediction=torch.max(output.data,1)
                assert prediction == torch.tensor([ans[i]])
