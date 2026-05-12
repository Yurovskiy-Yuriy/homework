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
    
    
stack_1 = Stack()
print(stack_1.is_empty())  # True

stack_1.push('1')
stack_1.push('2')
stack_1.push('3')
print(stack_1.peek())      # '3'

stack_1.pop()              # 
print(stack_1.peek())      # '2'
print(stack_1.is_empty())  # False

stack_1.push('045')
print(stack_1.peek())      # '045'
print(stack_1.size())      #  3
    