# HealthCheck: Ваш помощник в заботе о здоровье

HealthCheck - это телеграм-бот, который предоставляет пользователям удобный инструмент для самодиагностики и поиска необходимой медицинской информации. 

## Функционал:

· Регистрация пользователя:
* Создание профиля.
* Безопасное хранение данных пользователя.

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
 

## Преимущества:

· Доступность:  Бот доступен 24/7 в Telegram. 

· Анонимность:  Данные пользователей хранятся анонимно. 

· Удобство:  Простой и интуитивно понятный интерфейс. 

· Информативность:  Предлагает полезную информацию о симптомах и лечении различных заболеваний. 

## Важно:

· HealthCheck - это инструмент самодиагностики, а не замена медицинской консультации.  
· Если вы подозреваете у себя какое-либо заболевание, обратитесь к врачу.

Следите за развитием проекта!  В будущем HealthCheck будет расширять свою функциональность и предлагать новые возможности для пользователей. 


##  Используемые технологии

Backend:

· Python, PostgreSQL, RabbitMQ

Machine Learning:

· PyTorch, TensorFlow, XGBoost

Дополнительные технологии:

· aiogram

## Структура проекта:
core: -- основной код бота
* handlers: -- хэндлеры телеграм бота
  * brain_test.py -- анализ МРТ
  * change_user_data.py -- изменение данных пользователя
  * delete_acc.py -- удаление аккаунта
  * dialogue_with_doctor.py -- переход в диалог с врачем
  * full_checkup.py -- тест на большое число заболеваний
  * main_menu.py -- обработчик кнопок главного меню
  * registration.py -- регистрация пользователя
  * show_hospital.py -- показ больниц на карте
  * show_test_results.py -- показать результаты тестов
  * start.py -- скрипт на команду старт
  * xray_test.py -- анализ флюорографии

* keyboards:
  * keyboards.py -- клавиатуры для телеграм бота
 
* ml:
  * Diabetes_model-2.pkl -- модель для анализа диабета
  * full_ml.pth -- модель для анализа полного теста
  * x_ray_effnet_b.h5 -- модель для анализа флюорографии
* brain_analysis.py -- скрипт для обработки результатов анализа МРТ
* config.py -- обработчик config-a
* config.yaml -- конфигурационный файл
* diabetes_analysis.py -- скрипт для обработки результатов теста на диабет
* fullcheck_analysis.py -- скрипт для обработки результатов полного теста
* hash.py -- скрипт для хэширования id пользователей и названия изображений
* rpc_client.py -- класс для работы с rabbitm
* sql_utils.py -- функции для работы с postgresqp
* states.py -- состояния для телеграм бота
* xray_analysis.py -- скрипт для обработки результатов флюорографии

image -- папка для хранения изображений, присланых пользователей

test: -- директория с тестами
* results -- директория с результатами тестов
* test_images -- директория с изображениями для тестов
* test_memory_usage_brain_analysis.py -- тест на использование RAM нейросети для анализа МРТ
* test_memory_usage_diabetes_analysis.py -- тест на использование RAM ml для анализа теста на диабет
* test_memory_usage_fullckeck_analysis.py -- тест на использование RAM ml для анализа результатов полного теста
* test_memory_usage_xray_analysis.py -- тест на использование RAM нейросети для анализа флюорографии
* test_model_brain_analysis.py -- тест загрузки и работоспособности нейросети для анализа МРТ
* test_model_diabetes_analysis.py -- тест загрузки и работоспособности ml для анализа теста на диабет
* test_model_fullcheck_analysis.py -- тест загрузки и работоспособности нейросети для анализа результатов полного теста
* test_model_xray_analysis.py -- тест загрузки и работоспособности нейросети для анализа флюорографии
  
main.py -- запуск телеграм бота

requirements.txt -- файл с зависимостями

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
   * python3 main.py  # Запустить бота
   * python3 brain_analysis.py
   * python3 xray_analysis.py
   * python3 diabetes_analysis.py
   * python3 fullcheck_analysis.py