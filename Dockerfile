FROM python:3.11-slim-bullseye

# Отключаем запись .pyc файлов и буферизацию вывода (лучше для Docker)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 1. Делаем корневую папку проекта
WORKDIR /code

# Копируем зависимости и устанавливаем их
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 2. Копируем папку app ВНУТРЬ папки /code. 
# Теперь структура внутри контейнера будет: /code/app/app.py
COPY ./app /code/app

# 3. Запускаем uvicorn. Теперь он корректно найдет пакет 'app' и модуль 'app' внутри него
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "80"]