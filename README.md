
# Сервис объявлений на FastAPI

Результатом работы является асинхронный API для управления объявлениями (CRUD + поиск), написанный на FastAPI с использованием SQLAlchemy (asyncio) и PostgreSQL.

Проект полностью контейнеризирован с помощью Docker Compose.

## Быстрый старт

### 1. Создать и настроить файл .env

Создайте файл `.env` в корне проекта со следующими настройками (или убедитесь, что он уже заполнен):

POSTGRES_USER=<имя>
POSTGRES_PASSWORD=<пароль>
POSTGRES_DB=advertisement_db
POSTGRES_PORT=5432
POSTGRES_HOST=postgres

### 2. Собрать образы и запустить контейнеры

Выполните команду в корне проекта (где лежит docker-compose.yaml):

docker-compose up --build -d

*Флаг `--build` обязателен при первом запуске или после изменения кода/зависимостей. Флаг `-d` запускает контейнеры в фоновом режиме.*

### 3. Проверить статус контейнеров

docker-compose ps

Оба контейнера (api и postgres) должны быть в статусе Up. У PostgreSQL также должен быть статус (healthy).

---

## Тестирование API (Как делать запросы)

Есть три удобных способа проверить работу роутов.

### Способ 1: Встроенный Swagger UI (Рекомендуется)

FastAPI автоматически генерирует интерактивную документацию.

1. Откройте в браузере: http://localhost:8080/docs
2. Выберите нужный метод (например, POST /v1/advertisement).
3. Нажмите кнопку "Try it out".
4. Вставьте тело запроса (пример ниже) и нажмите "Execute".
5. Посмотрите ответ сервера и код состояния (например, 200 OK или 409 Conflict).

### Способ 2: Примеры запросов через curl (Терминал)

# Создать объявление

curl -X POST http://localhost:8080/v1/advertisement 
  -H "Content-Type: application/json" 
  -d '{"title":"Велосипед", "description":"Горный, новый", "price":15000, "author":"Иван"}'

# Получить объявление по ID (например, ID=1)

curl http://localhost:8080/v1/advertisement/1

# Частично обновить объявление (изменить цену)

curl -X PATCH http://localhost:8080/v1/advertisement/1 
  -H "Content-Type: application/json" 
  -d '{"price": 18000}'

# Поиск объявлений (фильтрация)

curl "http://localhost:8080/v1/advertisement?q_title=велосипед&q_price_min=10000"

# Удалить объявление

curl -X DELETE http://localhost:8080/v1/advertisement/1

### Способ 3: Использование файла rest.http

Создайте в корне проекта файл `requests.http` (или `rest.http`) и вставьте туда следующий код. Большинство IDE (VS Code, PyCharm) покажут кнопку "Send Request" прямо над каждым запросом.

### Создать объявление

POST http://localhost:8080/v1/advertisement
Content-Type: application/json

{
  "title": "Ноутбук",
  "description": "Игровой, в отличном состоянии",
  "price": 85000,
  "author": "Алексей"
}

### Получить объявление по ID (замените 1 на реальный ID из ответа выше)

GET http://localhost:8080/v1/advertisement/1

### Обновить объявление (PATCH)

PATCH http://localhost:8080/v1/advertisement/1
Content-Type: application/json

{
  "price": 80000
}

### Поиск объявлений по параметрам

GET http://localhost:8080/v1/advertisement?q_title=Ноутбук&q_price_min=50000

### Удалить объявление

DELETE http://localhost:8080/v1/advertisement/1

---

## Остановка и очистка

Чтобы остановить контейнеры и полностью удалить все данные из базы данных (очистить volumes), выполните:

docker-compose down -v

*Внимание: флаг `-v` безвозвратно удалит все сохранённые объявления из PostgreSQL.*

Если нужно просто остановить сервисы с сохранением данных:

docker-compose down

---

## Структура проекта

FastApi_DZ/
├── app/
│   ├── __init__.py       # Делает папку Python-пакетом (обязательно!)
│   ├── app.py            # Точки входа, роуты и инициализация FastAPI
│   ├── config.py         # Настройки окружения
│   ├── models.py         # SQLAlchemy ORM модели
│   ├── schemas.py        # Pydantic схемы для валидации запросов/ответов
│   └── services.py       # Бизнес-логика и работа с БД
├── docker-compose.yaml   # Оркестрация контейнеров (API + PostgreSQL)
├── Dockerfile            # Инструкция для сборки образа API
├── requirements.txt      # Зависимости Python
├── .env                  # Переменные окружения (не коммитить в Git!)
└── README.md             # Этот файл
