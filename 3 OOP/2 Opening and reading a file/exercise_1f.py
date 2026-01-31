'''Задача №1
Должен получится следующий словарь
cook_book = {
  'Омлет': [
    {'ingredient_name': 'Яйцо', 'quantity': 2, 'measure': 'шт.'},
    {'ingredient_name': 'Молоко', 'quantity': 100, 'measure': 'мл'},
    {'ingredient_name': 'Помидор', 'quantity': 2, 'measure': 'шт'}
    ],
  'Утка по-пекински': [
    {'ingredient_name': 'Утка', 'quantity': 1, 'measure': 'шт'},
    {'ingredient_name': 'Вода', 'quantity': 2, 'measure': 'л'},
    {'ingredient_name': 'Мед', 'quantity': 3, 'measure': 'ст.л'},
    {'ingredient_name': 'Соевый соус', 'quantity': 60, 'measure': 'мл'}
    ],
  'Запеченный картофель': [
    {'ingredient_name': 'Картофель', 'quantity': 1, 'measure': 'кг'},
    {'ingredient_name': 'Чеснок', 'quantity': 3, 'measure': 'зубч'},
    {'ingredient_name': 'Сыр гауда', 'quantity': 100, 'measure': 'г'},
    ]
  }
'''
cook_book = {}
with open(r'd:\recipes.txt', encoding='utf-8') as f:
          for line in f:
              if '|' not in line and len(line) > 2:                       # если в строке есть символ '|' и строка больше двух символов тогда:
                  cook_book.setdefault(line.strip('\n'), [])     # создаем новый ключ с пустым значением
                  key = line.strip('\n')                         # запоминаем название ключа в переменную
              elif '|' in line:                                          # иначе если в строке есть символ '|'
                  line_remix = line.strip('\n').split('|')       # разбиваем строку на части используя '|' 
                  cook_book[key].append({'ingredient_name': line_remix[0].strip(' '), 'quantity': int(line_remix[1].strip(' ')), 'measure': line_remix[2].strip(' ')}) # добавляем в существующий ключ соответсвующие значения
print(cook_book)

'''
Результат:
{
  'Омлет': [
    {'ingredient_name': 'Яйцо', 'quantity': '2', 'measure': 'шт'},
    {'ingredient_name': 'Молоко', 'quantity': '100', 'measure': 'мл'}, 
    {'ingredient_name': 'Помидор', 'quantity': '2', 'measure': 'шт'}], 
  'Утка по-пекински': [
    {'ingredient_name': 'Утка', 'quantity': '1', 'measure': 'шт'}, 
    {'ingredient_name': 'Вода', 'quantity': '2', 'measure': 'л'},
    {'ingredient_name': 'Мед', 'quantity': '3', 'measure': 'ст.л'}, 
    {'ingredient_name': 'Соевый соус', 'quantity': '60', 'measure': 'мл'}
    ], 
  'Запеченный картофель': [
    {'ingredient_name': 'Картофель', 'quantity': '1', 'measure': 'кг'},
    {'ingredient_name': 'Чеснок', 'quantity': '3', 'measure': 'зубч'}, 
    {'ingredient_name': 'Сыр гауда', 'quantity': '100', 'measure': 'г'}
    ],
  'Фахитос': [
    {'ingredient_name': 'Говядина', 'quantity': '500', 'measure': 'г'}, 
    {'ingredient_name': 'Перец сладкий', 'quantity': '1', 'measure': 'шт'},
    {'ingredient_name': 'Лаваш', 'quantity': '2', 'measure': 'шт'},
    {'ingredient_name': 'Винный уксус', 'quantity': '1', 'measure': 'ст.л'}, 
    {'ingredient_name': 'Помидор', 'quantity': '2', 'measure': 'шт'}
    ]
  }
'''