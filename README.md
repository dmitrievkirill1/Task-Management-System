# TaskManagementSystem

Проект "Система управления задачами" представляет собой базу данных для эффективного отслеживания и управления задачами в командных проектах.

## Запуск проекта для разработки

- `python -m venv venv` - создание виртуального окружения

Для активации виртуального окружения:
- `venv\Scripts\activate.bat` - для Windows
- `source venv/bin/activate` - для Linux и MacOS

Далее:

- `pip install -r requirements.txt` - для установки зависимостей
- Для работы с PostgreSQL, скачиваем его с офицального сайта [PostgreSQL](https://www.postgresql.org/download/)
- `python manage.py migrate` - применение миграций
- `python manage.py runserver` - запуск сайта на локальном сервере по адресу http://127.0.0.1:8000/