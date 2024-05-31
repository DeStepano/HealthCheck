# HealthCheck (Телеграмм бот)

О проекте:  
Health Check - это телеграм бот, позволяющий выявлять наличие заболеваний, основываясь на результатах опросов и изображений медецинских анализов.  


Функционал:  
Регистрация пользователя  
Сохранение пользователя в базе данных  
Два теста для выявления заболевания сердечно-сосудистрой системы  
Функция для анализа заболеваний легких на основе анализа рентгеновских снимков  
Функция для анализа заболеваний мозга на основе анализа МРТ  


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


Гайд по установке:  
Этот гайд поможет вам установить и настроить проект HealthCheck.

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

· Следуйте инструкциям по установке PostgreSQL  по ссылке.
· Создайте пользователя с правами на создание таблиц:
    
bash
### Вход в командную строку PostgreSQL
sudo -u postgres psql

### Создание пользователя
CREATE ROLE your_user WITH LOGIN PASSWORD 'your_password';

### Предоставление прав на создание таблиц
   GRANT CREATE TABLE TO your_user;
   
    * Замените your hostname,your port, your_user, your_password и your database name на свои значения (host: 'localhost', port: '5432' -- по умолчанию).
· В файле config.yaml  введите:

* users_db:
  * host: 'your hostname'
  * port: 'your port'
  * user: 'your user'
  * password: 'your password'
  * database: 'your database name'

## 4.3. Настройка RabbitMQ

· Следуйте инструкциям по установке RabbitMQ по ссылке.
· В файле config.yaml  введите ваш  host  RabbitMQ.

## 5. Запуск

·  Теперь ваш проект HealthCheck готов к запуску. Вы можете использовать следующие команды:
    
bash
   python main.py  # Запустить бота
