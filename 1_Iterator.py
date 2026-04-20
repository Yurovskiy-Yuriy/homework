'''Доработать класс FlatIterator в коде ниже. Должен получиться итератор, 
который принимает список списков и возвращает их плоское представление, 
т. е. последовательность, состоящую из вложенных элементов.
Функция test в коде ниже также должна отработать без ошибок.'''

class FlatIterator:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        self.index = 0 # индекс колличества списков в списке
        self.index_in_list = 0 # индекс колличесва эллементов в списке
        
    def __iter__(self):
        return self

    def __next__(self):
       
        # проверяем, не превысили ли колличесва списков в списке
        while self.index < len(self.list_of_list):  
            # проверяем, не превысили ли колличесва элеменов в списке
            
            if self.index_in_list < len(self.list_of_list[self.index]):
                # запоминаем сам эллемент
                item = self.list_of_list[self.index][self.index_in_list]
                self.index_in_list += 1    
                return item
            else:
                self.index += 1
                self.index_in_list = 0

        raise StopIteration


def test_1():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


if __name__ == '__main__':
    test_1()

