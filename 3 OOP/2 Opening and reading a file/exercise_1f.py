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
import re

cook_book = {}
with open(r'd:\test\recipes.txt', encoding='utf-8') as f:
    for line in f:
        clean_line = line.strip()
        # Регулярное выражение для извлечения название блюда
        dish_re = r'^[А-Яа-яЁё\s\-]+$'
        dish = re.match(dish_re, clean_line)

        # Регулярное выражение для извлечения ингридиента
        ingredient_re = r'^(.+)\s+\|\s*(\d+)\s\|\s*(.+)$'
        ingredient = re.match(ingredient_re, clean_line)

        if dish:
            dish_result = dish.group()
            cook_book.setdefault(dish_result, []) # создаем название блюда

        if ingredient:
            ingredient_result, quantity, unit = ingredient.groups() # добавляем в название блюда ингридиенты 
            cook_book[dish_result].append({'ingredient_name': ingredient_result, 'quantity': quantity, 'measure': unit})
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