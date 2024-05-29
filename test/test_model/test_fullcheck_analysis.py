import json
import pika
import time
import asyncio
import torch
import torch.nn as nn
from torch import load
from torch.optim import Adam
import pandas as pd


class CustomModel(nn.Module):
    def init(self):
        super(CustomModel, self).init()
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
criterion = nn.BCELoss()
optimizer = Adam(model_fullcheck.parameters())
model_fullcheck = load('/home/sasha/health_checker/HealthCheck/core/ml/full_ml.pth')
model_fullcheck.eval()


def test_loading():
    assert isinstance(model_fullcheck, nn.Module)


def test_first_sample():
    df = pd.read_pickle("/home/sasha/health_checker/HealthCheck/test/test_model/data/data_norm0.25.pkl")
    df = df[0:2]
    input = df["INPUT"]
    output = df["OUTPUT"]
    res = model_fullcheck.forward(torch.tensor(input[0]).float()).detach().numpy().tolist()
    assert res == output[0]
