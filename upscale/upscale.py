#upscale/upscale.py
import os
import cv2
import numpy as np
from cv2 import dnn_superres

# Глобальная переменная для хранения экземпляра модели (Синглтон)
_scaler = None

def get_scaler(model_path: str = None) -> dnn_superres.DnnSuperResImpl:
    global _scaler
    if _scaler is None:
        # ### ДОРАБОТКА: Если путь не передан, автоматически находим модель рядом с этим файлом
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), 'EDSR_x2.pb')
        
        _scaler = dnn_superres.DnnSuperResImpl_create()
        _scaler.readModel(model_path)
        _scaler.setModel("edsr", 2)
    return _scaler

def upscale(input_path: str, output_path: str, model_path: str = None) -> None:
    """
    Старая функция (для обратной совместимости)
    """
    if model_path is None:
        model_path = os.path.join(os.path.dirname(__file__), 'EDSR_x2.pb')
        
    scaler = get_scaler(model_path)
    image = cv2.imread(input_path)
    result = scaler.upsample(image)
    cv2.imwrite(output_path, result)

def upscale_bytes(input_bytes: bytes, model_path: str = None) -> bytes:
    """
    Новая функция для обработки изображений целиком в памяти (без диска)
    """
    if model_path is None:
        model_path = os.path.join(os.path.dirname(__file__), 'EDSR_x2.pb')
        
    scaler = get_scaler(model_path)
    
    # Декодируем байты в массив numpy (формат OpenCV)
    nparr = np.frombuffer(input_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if image is None:
        raise ValueError("Не удалось декодировать изображение из байтов")
    
    # Выполняем апскейлинг
    result = scaler.upsample(image)
    
    # Кодируем результат обратно в байты (формат PNG)
    success, encoded_image = cv2.imencode('.png', result)
    if not success:
        raise RuntimeError("Не удалось закодировать результат в PNG")
        
    return encoded_image.tobytes()

def example():
    upscale('lama_300px.png', 'lama_600px.png')

if __name__ == '__main__':
    example()