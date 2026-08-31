# Домашнее задание к лекции «Docker Compose»



## Задание* (необязательное)

Cделать конфигурацию docker-compose любого Вашего проекта из курса по Django, который использует БД (например, CRUD: Склады и запасы).

Результатом является docker-compose.yml файл с описанием конфигурации для развертывания приложения (и не забудьте про Dockerfile).

P.S. для создания конфигурации необходим образ своего проекта, а значит предварительно необходимо описать Dockerfile, сделать образ и потом уже писать docker-compose.yml (это типичный сценарий при работе с Docker и Docker Compose).

---

## Решение:   

## Магазин телефонов - Django App

#### 1. Клонировать репозиторий

#### 2. Скопировать и настроить .env

cp .env.example .env

#### 3 Отредактировать .env со своими данными

Обязательные переменные в .env:
   SECRET_KEY=your-secret-key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DB_NAME=import_phones
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=db
   DB_PORT=5432

#### 4. Собрать

docker-compose build

#### 5. Запустить

docker-compose up -d

#### 6. Посмотреть логи (ошибок быть не должно!)

docker-compose logs db

#### 7. Проверить статус

docker-compose ps

#### Доступ

•	Веб-приложение: http://localhost


