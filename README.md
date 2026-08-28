# Домашнее задание к лекции «Docker»



## Задание 1

По аналогии с практикой из лекции создайте свой docker image с http сервером nginx. Замените страницу приветствия Nginx на своё (измените текст приветствия на той же странице).

---

## Решение:   \docker-nginx-hw

В этом репозитории находится Docker-образ, который запускает веб-сервер Nginx со своей HTML-страницей вместо стандартной страницы приветствия.

**Файл index.html** — наша страница.
**Файл Dockerfile** — инструкции по сборке образа на базе nginx:alpine.

---

## Инструкция по запуску проекта

1. Склонируйте этот репозиторий
2. Перейдите в папку проекта

   ```bash
   cd docker-nginx-hw
   ```
3. Соберите образ:

   ```bash
   docker build -t my-name/nginx-custom.0.1 .
   ```
4. Запустите контейнер:

   ```bash
   docker run --name my-test-server -d -p 8090:80 my-name/nginx-custom.0.1
   ```
5. Проверьте результат в браузере по адресу:
   http://localhost:8090


## Задание 2

Создайте контейнер для REST API сервера любого вашего проекта из курса по Django (например, CRUD: Склады и запасы).

Проверьте конфигурацию Django на использование переменных окружения (environment).

Приложите в репозиторий Dockerfile и файлы приложения.

В README.md описать типовые команды для запуска контейнера c backend-сервером.
Для проверки работоспособности вашего контейнера отправляйте запросы с помощью VS Code REST Client или Postman.

## Решение:   phones\

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

•	Веб-приложение: http://localhost:8000
•	Админ-панель: http://localhost:8000/admin/

#### Тестирование API

Использовать Postman или VS Code REST Client:
http
GET http://localhost:8000/
GET http://localhost:8000/phone/1/
