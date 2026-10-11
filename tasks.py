# tasks.py
import os
import base64
from celery import Celery
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from upscale.upscale import upscale_bytes

broker_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
result_backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

celery_app = Celery('tasks', broker=broker_url, backend=result_backend)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'upscale', 'EDSR_x2.pb')

@celery_app.task
def process_upscale_task(input_bytes: bytes) -> str:
    """
    Фоновая задача апскейлинга.
    ### ДОРАБОТКА: Возвращаем результат в base64, чтобы Celery мог его сериализовать в JSON
    """
    result_bytes = upscale_bytes(input_bytes, model_path=MODEL_PATH)
    
    # ### ДОРАБОТКА: Кодируем bytes в base64 (строка), чтобы JSON мог это сохранить
    return base64.b64encode(result_bytes).decode('utf-8')