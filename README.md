## HealthCheck: Ваш помощник в заботе о здоровье

HealthCheck - это телеграм-бот, который предоставляет пользователям удобный инструмент для самодиагностики и поиска необходимой медицинской информации. 

Функционал:

# Регистрация пользователя: 

   Создание профиля.
   Безопасное хранение данных пользователя.
· Хранение результатов анализов:  

    * Загрузка и сохранение результатов анализов, таких как флюорография и МРТ.
· Тесты для выявления заболеваний:

    * Тест на диабет:  Помогает оценить риск развития диабета.
    * Тест на широкий спектр заболеваний:  Позволяет пользователям пройти тест на наличие различных заболеваний.
· Анализ медицинских изображений:

    * Анализ флюорографии:  Определение признаков заболеваний легких.
    * Анализ МРТ:  Определение признаков заболеваний мозга.
· Консультация с врачом: 

    * Возможность перейти в диалог с врачом для получения консультации.
· Карта больниц: 

    * Веб-приложение, позволяющее пользователям просматривать местоположение больниц в Санкт-Петербурге, специализирующихся на диагностировании и лечении различных заболеваний. 

Преимущества:

· Доступность:  Бот доступен 24/7 в Telegram. 
· Анонимность:  Данные пользователей хранятся анонимно. 
· Удобство:  Простой и интуитивно понятный интерфейс. 
· Информативность:  Предлагает полезную информацию о симптомах и лечении различных заболеваний. 

Важно:

· HealthCheck - это инструмент самодиагностики, а не замена медицинской консультации.  
· Если вы подозреваете у себя какое-либо заболевание, обратитесь к врачу.

Следите за развитием проекта!  В будущем HealthCheck будет расширять свою функциональность и предлагать новые возможности для пользователей. 


Используемые библиотеки и технологии:  
    Aiogram 3.3.0 - написание бота  
    SQLite 3.45.2 - базы данных  
    RabbitMQ 3.13.0 - сервис очередей  
    Pillow - работа с изображениями  
    Hashlib - шифрование  
    Pika 1.3.2 - работа с RabbitMQ в python  

Ссылки:  
https://docs.aiogram.dev - Aiogram  
https://www.sqlite.org - SQLite  
https://www.rabbitmq.com - RabbitMQ  


# Гайд по установке телеграм бота:  

## 1. Скачивание репозитория

· Клонируйте репозиторий HealthCheck:
    
bash
   git clone https://github.com/ваш_репозиторий.git   cd health_checker/HealthCheck
   
 
## 2. Создание виртуального окружения

· Создайте виртуальное окружение Python:
    
bash
   python3 -m venv .venv  # Или используйте другой инструмент, например, virtualenv   
 · Активируйте виртуальное окружение:
    
bash
   source .venv/bin/activate  # Для Linux/macOS
   
     
bash
   .venv\Scripts\activate  # Для Windows
   
 
## 3. Установка зависимостей

· Установите все необходимые библиотеки из файла requirements.txt:
    
bash
   pip install -r requirements.txt
   
 
## 4. Настройка конфигурации

### 4.1. Изменение пути

· Откройте файлы config.yaml и config.py.
· Измените значение path  на путь к директории, где расположен проект.

### 4.2. Настройка PostgreSQL

· Следуйте инструкциям по установке PostgreSQL  по ссылке -- https://cloud.vk.com/blog/postgresql-v-ubuntu-kak-ustanovit.
· Создайте пользователя с правами на создание таблиц:
    
bash
### Вход в командную строку PostgreSQL
sudo -u postgres psql

### Создание пользователя
CREATE ROLE your_user WITH LOGIN PASSWORD 'your_password';

### Предоставление прав на создание таблиц
   GRANT CREATE TABLE TO your_user;
   
· В файле config.yaml Замените your hostname,your port, your_user, your_password и your database name на свои значения (host: 'localhost', port: '5432' -- по умолчанию):

* users_db:
  * host: 'your host'
  * port: 'your port'
  * user: 'your user'
  * password: 'your password'
  * database: 'your database name'

## 5. Настройка RabbitMQ

· Установке RabbitMQ, следуя инструкциям -- https://www.rabbitmq.com/docs/install-debian.
· В файле config.yaml  введите ваш  host  RabbitMQ.

* rpc_client:
  * host: 'your host'
  * queues:
    * brain_queue: brain_queue
    * xray_queue: xray_queue
    * first_check_queue: first_check
    * second_check_queue: second_check
    * fullcheck_queue: fullcheck

## 6. Запуск
Запустите main.py для запуска бота
Запустите brain_analysis.py для запуска обработки анализов МРТ
Запустите xray_analysis.py для запуска обработки анализов флюорографии
Запустите diabetes_analysis.py для запуска обработки анализов на диабет
Запустите fullcheck_analysis.py для запуска обработки анализов полного теста
    
bash
   python3 main.py  # Запустить бота
   python3 brain_analysis.py
   python3 xray_analysis.py
   python3 diabetes_analysis.py
   python3 fullcheck_analysis.py
