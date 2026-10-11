# Тесты для проверки API

import io
import pytest
from app import app
from tasks import process_upscale_task

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Отключаем реальный вызов Celery для тестов, чтобы они работали быстро
    app.config['CELERY_TASK_ALWAYS_EAGER'] = True
    app.config['CELERY_TASK_EAGER_PROPAGATES'] = True
    
    with app.test_client() as client:
        yield client

def test_upscale_endpoint_accepts_file(client):
    """Тест проверяет, что эндпоинт принимает файл и возвращает task_id"""
    # Создаем фиктивные байты изображения
    fake_image_bytes = b'fake_image_data_for_testing'
    data = {
        'file': (io.BytesIO(fake_image_bytes), 'test.png')
    }
    
    response = client.post('/upscale', data=data, content_type='multipart/form-data')
    
    assert response.status_code == 202
    json_data = response.get_json()
    assert 'task_id' in json_data

def test_upscale_endpoint_rejects_no_file(client):
    """Тест проверяет обработку отсутствия файла"""
    response = client.post('/upscale', data={}, content_type='multipart/form-data')
    assert response.status_code == 400
    assert response.get_json()['error'] == "No file part"