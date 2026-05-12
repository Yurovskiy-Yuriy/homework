class Stack:
    def __init__(self):
        self.stack_list = []
        
    # проверка стека на пустоту
    def is_empty(self):
        return len(self.stack_list) == 0
    
    # добавление нового элемента на вершину стека
    def push(self, element):
        self.stack_list.append(element)
        
    # удаление верхнего элемента стека
    def pop(self):
        if self.is_empty():  # Проверяем, не пуст ли стек, чтобы избежать ошибки
            return None
        return self.stack_list.pop()

    # возвращение верхнего элемента стека, но не удаляет его
    def peek(self):
        if self.is_empty(): # # Проверяем, не пуст ли стек, чтобы избежать ошибки
            return None
        return self.stack_list[-1]
    
    # возвращение количества элементов в стеке
    def size(self):
        return len(self.stack_list)
    
    
    
if __name__ == '__main__':

    element_dict = {'(': ')', '[': ']', '{': '}'}
    
    def balanced_list(input_string):
        
        stack = Stack()
        is_balanced = True
    
        for x in input_string:
            
            if x in element_dict: # проверяяем существует ли такой ключ в словаре
                stack.push(x)
            #добавляем до тех пор пока не сработает следующяя проверка
            
            elif x in element_dict.values(): # проверяем, что текущий символ- закрывающяя скобка
                if stack.is_empty(): # пустой ли стек
                    is_balanced = False # стек пустой, а у нас появилась закрывающяя скобка
                    break 
                
                last_open = stack.pop() # удаляем последний эллемент и запоминаем его
                if element_dict[last_open] != x: # если значение его ключа в словаре не равно самому ему то: 
                    is_balanced = False
                    break
            

        if not stack.is_empty(): # проверка на остаток скобок в стеке
            is_balanced = False
        
        if is_balanced:
            return 'Сбалансированно'
        else:
            return 'Несбалансированно'
    
    
    print(balanced_list('{{[()]}}'))
    print(balanced_list('[([])((([[[]]])))]{()}'))
    print(balanced_list('{{[()]}}'))
    
    print(balanced_list('}{}'))
    print(balanced_list('{{[(])]}}'))
    print(balanced_list('[[{())}]'))