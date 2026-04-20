'''Доработать функцию flat_generator. Должен получиться генератор, 
который принимает список списков и возвращает их плоское представление.
 Функция test в коде ниже также должна отработать без ошибок.'''

import types


def flat_generator(list_of_lists):

    index = 0 # индекс колличества списков в списке
    index_in_list = 0 # индекс колличесва эллементов в списке


    # проверяем, не превысили ли колличесва списков в списке
    while True:
        if index >= len(list_of_lists): 
            return 
           
        # проверяем, не превысили ли колличесва элеменов в списке
        if index_in_list < len(list_of_lists[index]):
            # запоминаем сам эллемент
            yield list_of_lists[index][index_in_list]
            index_in_list += 1    
            
        else:
            index += 1
            index_in_list = 0
            
def test_2():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)


if __name__ == '__main__':
    test_2()
    