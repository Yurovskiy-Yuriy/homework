'''Задача №2
  Нужно написать функцию, которая на вход принимает список блюд из 
  cook_book  и количество персон для кого мы будем готовить
get_shop_list_by_dishes(dishes, person_count)

  На выходе мы должны получить словарь с названием ингредиентов и его количества для блюда.
Например, для такого вызова
get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2)

  Должен быть следующий результат:
{
  'Картофель': {'measure': 'кг', 'quantity': 2},
  'Молоко': {'measure': 'мл', 'quantity': 200},
  'Помидор': {'measure': 'шт', 'quantity': 4},
  'Сыр гауда': {'measure': 'г', 'quantity': 200},
  'Яйцо': {'measure': 'шт', 'quantity': 4},
  'Чеснок': {'measure': 'зубч', 'quantity': 6}
}
Обратите внимание, что ингредиенты могут повторяться

'''
cook_book = {
  'Омлет': [
    {'ingredient_name': 'Яйцо', 'quantity': '2', 'measure': 'шт'},
    {'ingredient_name': 'Молоко', 'quantity': '100', 'measure': 'мл'},
    {'ingredient_name': 'Помидор', 'quantity': '2', 'measure': 'шт'}
    ],
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

def get_shop_list_by_dishes(dishes, person_count):
    shop_list = {}                                       # итоговый словарь
    
    for dish in dishes: # т.к. в первом задании написано, что колличесво ингридиентов в списке указанно не на одного человека, то будем это учитывать
        if dish == 'Омлет' or dish == 'Запеченный картофель':
            x = 3
        elif dish == 'Утка по-пекински':
            x = 4
        elif dish == 'Фахитос':
            x = 5
        
        for ingredient in cook_book[dish]:             # проходим по ингридиентам 
            ing = {}                             # временный словарь для хранения одного ингридиента
            quantity = (int(ingredient['quantity'])) / x * person_count                     # расчет колличества ингридиента с учетом колличества персон
            ing.setdefault(ingredient['ingredient_name'], {'measure': (ingredient['measure']), 'quantity': round(quantity, 1)})      # создаем ингридиент 
            if ingredient['ingredient_name'] not in shop_list:                  # проверяем, есть ли такой ингридиент в списке
                shop_list.update(ing)
            else:
                shop_list.get(ingredient['ingredient_name'])['quantity'] += round((int(ingredient['quantity'])) / x * person_count) # запрашиваем ключ в сушествующем ингридиенте и обновляем его c учетом колличества перон                               
    return shop_list
                 
print(get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2))
print()
print(get_shop_list_by_dishes(['Фахитос', 'Омлет'], 3))

