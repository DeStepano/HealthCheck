import torch
import torch.nn as nn
from torch import load
from torch.optim import Adam
import pandas as pd
from memory_profiler import profile


path = "your project path"


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
model_fullcheck = load(f"{path}/HealthCheck/core/ml/full_ml.pth")
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

@profile
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


def test_memory_usage():
    df = pd.read_pickle(f"{path}/HealthCheck/test/test_model/data/data_norm0.25.pkl")
    df = df[0:2]
    input = df["INPUT"]
    fullcheck_analysis(input[0])


if __name__ == "__main__":
    test_memory_usage()
