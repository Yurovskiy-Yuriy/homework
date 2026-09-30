# Домашнее задание к лекции «Создание REST API на FastApi» часть 1

## (Доработка)

Все исправления отмечены как     # ИСПРАВЛЕНО

## Задание

Вам нужно написать на fastapi и докеризировать сервис объявлений купли/продажи.

У объявлений должны быть следующие поля:

- заголовок
- описание
- цена
- автор
- дата создания

Должны быть реализованы следующе методы:

- Создание: POST /advertisement
- Обновление: PATCH /advertisement/{advertisement_id}
- Удаление: DELETE /advertisement/{advertisement_id}
- Получение по id: GET  /advertisement/{advertisement_id}
- Поиск по полям: GET /advertisement?{query_string}
- Авторизацию и аутентификацию реализовывать не нужно

Результатом работы является асинхронный API для управления объявлениями (CRUD + поиск), написанный на FastAPI с использованием SQLAlchemy (asyncio) и PostgreSQL.

Проект полностью контейнеризирован с помощью Docker Compose.

## Решение

### 1. Создать и настроить файл .env

Создайте файл `.env` в корне проекта со следующими данными:

POSTGRES_USER=<имя>
POSTGRES_PASSWORD=<пароль>
POSTGRES_DB=advertisement_db
POSTGRES_PORT=5432
POSTGRES_HOST=postgres

### 2. Собрать образы и запустить контейнеры

Выполните команду в корне проекта (где лежит docker-compose.yaml):

docker-compose up --build -d

### 3. Проверить статус контейнеров

docker-compose ps

Оба контейнера (api и postgres) должны быть в статусе Up.

---

## Тестирование API

### Встроенный Swagger UI

1. Откройте в браузере: http://localhost:8080/docs
2. Выберите нужный метод (например, POST /v1/advertisement).
3. Нажмите кнопку "Try it out".
4. Вставьте тело запроса (пример ниже) и нажмите "Execute".
5. Посмотрите ответ сервера и код состояния (например, 200 OK или 409 Conflict).
