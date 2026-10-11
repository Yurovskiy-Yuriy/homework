# Тесты для проверки оптимизации загрузки модели.

import pytest
from upscale.upscale import get_scaler

def test_scaler_is_singleton():
    scaler1 = get_scaler()
    scaler2 = get_scaler()
    
    # Проверяем, что это один и тот же экземпляр класса (один и тот же адрес в памяти)
    assert scaler1 is scaler2