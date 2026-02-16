import requests
from tqdm import tqdm 
from datetime import datetime
import json

result_files = [] # Список всех загруженных файлов

def create_folder(token): 
    #Создаем папку:
    url = 'https://cloud-api.yandex.net/v1/disk/resources'
    params = {'path': 'PY-144'}
    headers = {'Authorization': f'OAuth {token}'}

    print('Cоздаем папку на Яндекс.Диске....')

    response = requests.put(url, params=params, headers=headers)
    if response.status_code not in (201, 409):
            if response.status_code == 401:
                print('\nОшибка авторизации! Проверьте токен')
            raise RuntimeError(f'Не удалось создать папку "PY-144"')
    else:
        print('Папка "PY-144" успешно создана!')

def upload_file(token, text):
    headers = {'Authorization': f'OAuth {token}'}
    
    # скачиваем картинку
    print('Загрузка изображения из https://cataas.com/ ....')
    url =  f'https://cataas.com/cat/says/{text}' 
    response_img = requests.get(url)
    
    # определяем размер картинки
    image_size_bytes = len(response_img.content)   
    print(f"Изображение успешно загружено!")
    print()
    

    # -------------загружаем картинку на Yandex Disk:--------------
    current_time = datetime.now() # определяем текущее вроемя для названия изображения
    formatted_time = current_time.strftime("%d.%m.%Y %H:%M:%S")
    formatted_time = formatted_time.translate(str.maketrans(".: ", "___"))

    disk_path = f'/PY-144/котик_{formatted_time}.jpg'  # куда загружаем
    image = f'котик_{formatted_time}.jpg'
   
    # получаем временную ссылку на загрузку:
    response_get = requests.get(
        'https://cloud-api.yandex.net/v1/disk/resources/upload',
        params = {'path': disk_path, 'overwrite': 'true'},
        headers=headers)
    
    # проверяем успешность получения ссылки
    if response_get.status_code != 200:
        raise RuntimeError(f"Ошибка получения ссылки для загрузки: {response_get.text}")
    
    # извлекаем из JSON-ответа поле href — временную URL-ссылку, по которой загружаем файл
    upload_link = response_get.json()['href']

    # начинаем отправку файла с отображением прогресса
    with tqdm(total=image_size_bytes, unit='B', unit_scale=True, desc="Загрузка изображения на Яндекс.Диск") as pbar:
        def generate_data(data):
            start_pos = 0
            chunk_size = 8192  # устанавливаем размер блока чтения 8 Кб
            while start_pos < len(data):
                end_pos = min(start_pos + chunk_size, len(data))
                yield data[start_pos:end_pos]
                pbar.update(end_pos - start_pos)
                start_pos = end_pos

        # отправляем изображение кусочками
        response_put = requests.put(upload_link, data=generate_data(response_img.content), headers=headers)

    #  Проверяем успех загрузки
    if response_put.status_code == 201:

        # подводим статистику
        result_files.append({
            "filename": image,
            "bytes": image_size_bytes,
            "text": text
            })

        print(f'\nИзображение "{image}" успешно загружено!')
        print(f"Размер изображения: {image_size_bytes} байт")

        # Делаем файл публичным
        publish_url = 'https://cloud-api.yandex.net/v1/disk/resources/publish'
        publish_response = requests.put(publish_url, params={'path': disk_path}, headers=headers)
        
        if publish_response.status_code == 200:
            print(f"Ссылка: https://disk.yandex.ru{disk_path}")
        else:
            print('Ошибка! Изображение не удалось сделать публичным')
        
    else:
        print(f'Изображение {image} не загружено')

if __name__ == '__main__':
    token = input("Введите ваш токен Яндекс.Диска: ").strip()
    create_folder(token)
    
    loading = 'y'
    while loading == 'y':
        text = input('Введите текст который будет на картинке: ')
        upload_file(token, text)

        while True:
            loading = input('\nЖелаете еще скачать картинку (y/n)? ').lower().strip()
            if loading in ['y', 'n']:
                break
            print("Введите только 'y' или 'n'!")  

    # сохраняем все в json-файл
    with open('stats.json', 'w', encoding='utf-8') as f:
        json.dump(result_files, f, indent=2, ensure_ascii=False)
    
    # подводим общюю статистику:
    with open('./stats.json', encoding='utf-8') as f:
        json_data = json.load(f)  

    print()
    print(f'Всего загружено файлов: {len(json_data)}')
    list_bytes = [item['bytes'] for item in json_data]
    print(f'Общий размер всех файлов: {sum(list_bytes)} bytes')

