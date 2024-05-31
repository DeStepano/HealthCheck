## Web App: Карта больниц

Это веб-приложение для телеграм-бота, которое позволяет просматривать на Яндекс.Картах местоположение больниц, специализирующихся на лечении и диагностировании различных заболеваний.


## Используемые технологии


Backend:

· Python, Flask, SQLAlchemy,

Frontend:

· HTML, CSS, JavaScript: 

Инфраструктура:

· Nginx, Gunicorn

API:

· Яндекс Карты API


## Структура проекта:

 health_checker/HealthCheck/
├── instance
│   └── hospital.db  # База данных больниц
├── static
│   ├── script.js  # Скрипт для отображения больниц на Яндекс Картах
│   └── style.css  # Стили для страниц
├── templates
│   ├── create_hospital.html  # Страница для добавления новой больницы
│   ├── index.html  # Начальная страница
│   └── map.html  # Страница с Яндекс Картой
├── requirements.txt  # Список зависимостей
└── web_app
    └── web_app.py  # Flask-сервер для обработки запросов


### Установка

1. Скачивание репозитория:
   
shell

    git clone https://github.com/ваш_репозиторий.git
   cd health_checker/HealthCheck/web
    
2. Создание виртуального окружения:

   * Создайте виртуальное окружение Python:
     
shell

      python3 -m venv .venv  
      
   * Активируйте виртуальное окружение:
     
shell

      source .venv/bin/activate  # Для Linux/macOS
      
     
powershell

      .venv\Scripts\activate  # Для Windows
      

3. Установка зависимостей:

   * Установите все необходимые библиотеки из файла requirements.txt:
     
shell

      pip install -r requirements.txt


4. Запуск веб-приложения:

   * Запустите файл web_app.py  с помощью nginx  и gunicorn  или других веб-серверов.
   * Пример с  gunicorn: 
      
shell

       gunicorn --bind 0.0.0.0:8000 web_app:app
       
      * Замените  0.0.0.0:8000  на ваш адрес и порт.

5. Настройка SSL-сертификата:

   * Получите SSL-ключ для вашего подключения с помощью  certbot:
     
shell

      certbot certonly --standalone -d ваш_домен 
      
     *  Замените  ваш_домен  на ваш домен.
   *  Настройте  nginx  для использования полученного SSL-сертификата.

### Важно:

·  Telegram  не может подключаться по незащищенному соединению (HTTP), поэтому вам  необходимо  использовать SSL-сертификат.
