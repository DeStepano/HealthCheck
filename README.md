# HealthCheck: Ваш помощник в заботе о здоровье

HealthCheck - это телеграм-бот, который предоставляет пользователям удобный инструмент для самодиагностики и поиска необходимой медицинской информации. 

## Функционал:

<<<<<<< HEAD
Функционал:  
Регистрация пользователя,  
Создание профиля пользователя в базе данных,
Два теста для выявления заболевания сердечно-сосудистрой системы,  
Определение пневмонии на основе флюорографии,
Классификация опухолей на основе снимков МРТ,
Выявление 49 различных заболеваний по обширному списку симптомов,
Диагностирование диабета у пациентов по опросу.

Планы на будущее:
Продать проект
=======
- **Регистрация пользователя:**
  - Создание профиля.
  - Безопасное хранение данных пользователя.

- **Хранение результатов анализов:**
  - Загрузка и сохранение результатов анализов, таких как флюорография и МРТ.

- **Тесты для выявления заболеваний:**
  - Тест на диабет: Помогает оценить риск развития диабета.
  - Тест на широкий спектр заболеваний: Позволяет пользователям пройти тест на наличие различных заболеваний.

- **Анализ медицинских изображений:**
  - Анализ флюорографии: Определение признаков заболеваний легких.
  - Анализ МРТ: Определение признаков заболеваний мозга.
  - Проверка по фото родинки на злокачественность.
>>>>>>> main

- **Консультация с врачом:**
  - Возможность перейти в диалог с врачом для получения консультации.

- **Карта больниц:**
  - Веб-приложение, позволяющее пользователям просматривать местоположение больниц в Санкт-Петербурге, специализирующихся на диагностировании и лечении различных заболеваний.

- **Машинное обучение:**
  - Распознавание сердечно-сосудистых заболеваний по данным о здоровье человека.
  - Распознавание диабета по общим данным о здоровье человека.

<<<<<<< HEAD
Гайд по установке:  
Coming soon!
=======
## Преимущества:

- **Доступность:** Бот доступен 24/7 в Telegram.
- **Анонимность:** Данные пользователей хранятся анонимно.
- **Удобство:** Простой и интуитивно понятный интерфейс.
- **Информативность:** Предлагает полезную информацию о симптомах и лечении различных заболеваний.

## Важно:

- **HealthCheck** - это инструмент самодиагностики, а не замена медицинской консультации.
- Если вы подозреваете у себя какое-либо заболевание, обратитесь к врачу.

Следите за развитием проекта! В будущем HealthCheck будет расширять свою функциональность и предлагать новые возможности для пользователей.

## Используемые технологии

**Backend:**
- Python, PostgreSQL, RabbitMQ

**Machine Learning:**
- PyTorch, TensorFlow, XGBoost

**Дополнительные технологии:**
- aiogram

## Классификация родинок:
Мы решали задачу с датасетом из 10,000 трэйновых изображений и 1,000 тестовых изображений, на которых изображены родинки, каждая из них помечена как доброкачественная или злокачественная. Для этого использовали передовую нейросеть от Facebook, созданную для классификации изображений. Также были опробованы более стандартные модели, но они не принесли значительных результатов. В итоге получились достаточно хорошие результаты, например: метрика recall составила 0.94.

## Классификация МРТ:
Был использован датасет с большим числом изображений, где каждое изображение должно было быть отнесено к одному из четырёх классов. Для решения этой задачи мы опробовали не только стандартные методы и модели, такие как ResNet и VGG, но и создали собственные модели. Результаты показали, что метрика recall для каждого из четырёх классов превысила 0.93, что свидетельствует об успешности нашей модели.

## Описание нейронной сети FullCheck:

Цель данной сети: прогнозировать возможные заболевания у человека по подробному описанию его симптомов.

Изначальные данные были представлены в тяжелом для анализа виде (https://huggingface.co/datasets/aai530-group6/ddxplus-french). Данные можно преобразовать в удобный вид с помощью Parquet (https://parquet.apache.org). В датасете около 1,300,000 строк данных (https://huggingface.co/datasets/aai530-group6/ddxplus).

Что представляют из себя симптомы? По сути мы имеем два типа симптомов: бинарные и categorical.
- **Бинарные** -- принимают значение true/false, то есть либо наличие данного симптома, либо отсутствие.
- **Categorical** -- с таким симптомом идёт дополнительный параметр, уточняющий характер проблемы.

Итого мы имеем 987 различных симптомов (с учётом уточняющих параметров) и 49 различных заболеваний. Данные необходимо преобразовать в нужный для обучения формат.

Симптомы были объединены в группы. Всего есть 227 вопросов.

Были проведены различные тесты архитектуры нейронной сети. Вот наиболее успешные примеры:
- Слой 1: 989 (activate relu) Слой 2: 49 (activate sigmoid)
- Слой 1: 989 (activate relu) Слой 2: 989 (activate relu) Слой 3: in 989/256 out 49 (activate sigmoid)

Оценка производилась при помощи метрик recall и precision. Цель приблизить precision к 0.5, чтобы уменьшить вероятность ложно-отрицательных результатов, а recall приблизить к 1. Оценка производилась на тестовых данных. Также был выбран под эти параметры threshold (0.1).

Лучший результат на тестовых данных:
- recall: 0.9748768172806537
- precision: 0.75

## Классификация родинок:
Мы решали задачу с датасетом из 10,000 трэйновых изображений и 1,000 тестовых изображений, на которых изображены родинки, каждая из них помечена как доброкачественная или злокачественная. Для этого использовали передовую нейросеть от Facebook, созданную для классификации изображений. Также были опробованы более стандартные модели, но они не принесли значительных результатов. В итоге получились достаточно хорошие результаты, например: метрика recall составила 0.94.

## Классификация МРТ:
Был использован датасет с большим числом изображений, где каждое изображение должно было быть отнесено к одному из четырёх классов. Для решения этой задачи мы опробовали не только стандартные методы и модели, такие как ResNet и VGG, но и создали собственные модели. Результаты показали, что метрика recall для каждого из четырёх классов превысила 0.93, что свидетельствует об успешности нашей модели.
>>>>>>> main
