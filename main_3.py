import bs4
import requests


from datetime import datetime
from functools import wraps

def logger(old_function):
    @wraps(old_function)
    def new_function(*args, **kwargs):

        # фиксируем время до вызва функции
        call_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        
        # собираем данные  до вызва функции
        func_name = old_function.__name__
        func_args = f"args: {args}, kwargs: {kwargs}"
        
        # вызваем функцию
        result = old_function(*args, **kwargs)

        # формируем лог
        log = (f'{call_time} '
            f'имя функции: {func_name}, '
            f'аргументы: {func_args}, '
            f'возвращаемое значение: {result}\n')

        # записываем в файл
        with open(r'main.log', 'a', encoding='utf-8') as file_out:  
            file_out.write(log)

        return result
    return new_function


@logger
def scrapping():
    result_news = []
    n = 0   # счетчик колличества найденных статей
    # список ключевых слов:
    KEYWORDS = ['дизайн', 'фото', 'web', 'python']

    # Отправляем GET-запрос к странице с играми на DTF
    response = requests.get('https://habr.com/ru/articles/')

    # Создаём объект BeautifulSoup для парсинга HTML-кода ответа
    soup = bs4.BeautifulSoup(response.text, features='lxml')

    # находим главный контейнер, в котором лежат все статьи.
    # Метод select_one возвращает только первый найденный элемент
    article_block = soup.select_one('div.tm-articles-list')

    # Внутри блока ищем все элементы с новостями (короткие посты).
    # select возвращает список всех подходящих элементов.
    if article_block:
        article_list = article_block.select('div.article-snippet')
    else:
        article_list = []

    # Проходим по каждому элементу из article_list (по каждой новости).
    for article in article_list:
        
        # внутри текущей статьи (article), ищем блок с заголовком и ссылкой внутри новости.
        div_with_link = article.select_one('a.tm-title__link')

        # Достаем значение атрибута href
        if not div_with_link:
            continue
        
        relative_link = div_with_link['href']
    
        # Собираем полную ссылку
        link = f'https://habr.com{relative_link}'
    
        # Получаем текст заголовка:
        title = div_with_link.text.strip()
    
        # Получаем время публикации
        time_tag = article.select_one('time')
        if time_tag:
            pub_time  = time_tag['title']
        else:
            pub_time  = 'Время не найдено'

        # Находим описание статьи
        preview_text_element = article.select_one('div.article-formatted-body')
        
        # Проверяем, нашли ли мы preview_text_element
        if preview_text_element:
            preview_text = preview_text_element.text.strip()
        else:
            preview_text = ''
                    
    # Переходим по ссылке и получаем HTML-страницу конкретной новости.
        article_response  = requests.get(link)
        # Парсим HTML этой страницы.
        article_soup = bs4.BeautifulSoup(article_response.text, features='lxml')

        text_block = article_soup.select_one('div.article-formatted-body')
    
        if text_block:
            # Удаляем лишние пробелы и переносы строк
            article_text = ' '.join(text_block.text.strip().split())
        else:
            article_text = 'Текст не найден'
        
        # Создаем одну строку для поиска, объединяя заголовок, текст анонса и текст статьи.
        search_string = f"{title} {preview_text} {article_text}".lower()
        
        # Ищем совпадения 
        for keyword in KEYWORDS:
            if keyword in search_string:
                n += 1
                result_news.append(pub_time + '\n' + title + '\n' + link + '\n' + article_text[:500])
                break

    result_news.append(f'Всего найдено {n} статей')
    print(result_news)

    return result_news

if __name__ == '__main__':
    scrapping()


