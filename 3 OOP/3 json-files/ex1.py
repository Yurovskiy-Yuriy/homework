'''Перед вами тренажёр, который позволит вам отточить навыки работы с файлами json.

Дан json-файл с новостями. Напишите функцию read_json, которая возвращает 
список из 10 самых часто встречающихся слов длиной не менее 6 символов. 
Приведение к нижнему регистру не требуется.
В результате корректного выполнения задания будет выведен следующий результат:

1
['туристов', 'компании', 'Wilderness', 'странах', 'туризма', 'которые', 'африканских', 'туристы', 'является', 'природы']

Содержание новостей находится в поле description в .json-файле. Объедините description всех новостей и выполните поиск слов.
'''



import json

def read_json(word_min_len=6, top_words_amt=10):
    with open(r'D:\newsafr.json', encoding='utf-8') as f:
        json_data = json.load(f) 


    news_list = json_data['rss']['channel']['items']

   
    result = []
    for x in news_list:  
        result.append(x['description'])
    result = ' '.join(result)
    result = result.split(' ')
    name = {}
    for x in result:
        if len(x) > 6:
            if x not in name:
                name.setdefault(x, 1)
            else:
                name[x] += 1

    top_10 = dict(sorted(name.items(), key=lambda x: x[1], reverse=True)[:10])
    top_10_list =[]
    for x in top_10.keys():
        top_10_list.append(x)
    return top_10_list

print(read_json())