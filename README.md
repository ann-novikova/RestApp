# NVK Haute Cuisine - RestApp

Веб-приложение для системы бронирования столиков в панорамном ресторане. Проект реализован на стеке Django + Django REST Framework с использованием JWT для авторизации и динамического фронтенда на JavaScript.

## Основные возможности

* Система бронирования: Интерактивная схема зала с выбором столиков в реальном времени.
* Авторизация и профиль: Регистрация, вход (через JWT) и личный кабинет пользователя.
* API: Полный программный интерфейс для управления пользователями и бронированиями.
* JWT-Auth Helper: Собственная JS-библиотека (Auth.api) для удобной работы с защищенными запросами и автоматическим обновлением токенов.
* Тестирование: Высокое покрытие кода тестами (авторизация, API, логика бронирования).

## Технологический стек

* Backend: Python 3.x, Django 5.x, Django REST Framework.
* Auth: SimpleJWT (JSON Web Tokens).
* Frontend: HTML5, Bootstrap 5, JavaScript (Fetch API).
* Database: PostgreSQL.
* DevOps: Docker, Docker Compose.

---

## Развертывание через Docker (Рекомендуется)

Проект полностью контейнеризирован. Для запуска вам понадобятся только Docker и Docker Compose.

1.  Клонируйте репозиторий:
    
shell

    git clone https://github.com/ann-novikova/RestApp.git
    cd RestApp
    

2.  Настройте переменные окружения:
    Создайте файл .env в корне проекта по образцу:
    
    DEBUG=True
    SECRET_KEY=your_secret_key
    DATABASE_NAME=
    DATABASE_USER=
    DATABASE_PASSWORD=
    DATABASE_HOST=
    DATABASE_PORT=
    

3.  Запустите проект:
    
shell

    docker-compose up --build
    
    Эта команда автоматически соберет образ, запустит базу данных, применит миграции и поднимет сервер на http://localhost:8000.

---

 💻 Локальная разработка (без Docker)

1.  Создайте виртуальное окружение и установите зависимости:
    
powershell

    python -m venv .venv
    source .venv/bin/activate  # Для Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    

2.  Выполните миграции и запустите сервер:
    
shell

    python manage.py migrate
    python manage.py runserver
    

---

## Тестирование и отчетность

Для запуска тестов используйте:
shell

python manage.py test

Для генерации отчета о покрытии кода (Coverage):
shell

coverage run --source='.' manage.py test
coverage html
После выполнения папка htmlcov будет содержать подробный отчет в формате HTML.

---

## API Endpoints (основные)


| Путь                        | Описание                                             |
|-----------------------------|------------------------------------------------------|
| `/users/api/register/`      | Регистрация нового пользователя                      |
| `/users/api/token/`         | Логин (получение Access и Refresh токенов)           |
| `/users/api/token/refresh/` | Обновление Access токена с помощью Refresh           |
| `/users/api/profile/`       | Получение данных текущего пользователя               |
| `/bookings/check/`          | Поиск свободных столов (параметры: date, start, end) |
| `/bookings/create/`         | Создание нового бронирования                         | 
| `/bookings/`                | Сервис для бронирования из 3 шагов                   | 
| `/`                         | Главная                                              | 
| `/about/`                   | О нас                                                | 




## Структура проекта

*  users/ — управление пользователями, кастомная модель User, JWT авторизация.
*  bookings/ — логика бронирования, проверка доступности и API столов.
*  content/ — управление контентом, информации о ресторане.
*  media/  — изображения ресторана.
*  static/ — CSS, кастомные скрипты (auth.js, login.js) и ресурсы.
*  templates/ — HTML шаблоны (интегрированные с Django Template Language).
*  Dockerfile & docker-compose.yml — конфигурация контейнеризации.

---
Разработано для NVK Panoramic Experience.
