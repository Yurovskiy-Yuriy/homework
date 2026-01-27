'''Задание № 1. Наследование.
У нас уже есть класс преподавателей и класс студентов. 
Студентов пока оставим без изменения, а вот преподаватели
бывают разные, поэтому теперь класс Mentor должен стать 
родительским классом, а от него нужно реализовать 
наследование классов Lecturer (лекторы) и Reviewer 
(эксперты, проверяющие домашние задания). 
Очевидно, имя, фамилия и список закрепленных курсов 
логично реализовать на уровне родительского класса. 
А чем же будут специфичны дочерние классы? Об этом в 
следующих заданиях. А пока можете проверить, что успешно 
реализовали дочерние классы'''

class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        
class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []
        
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

# Начало выполнения домашнего задания:  
class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
# Конец выполнения домашнего задания.  

'''best_student = Student('Ruoy', 'Eman', 'your_gender')
best_student.courses_in_progress += ['Python']
 
cool_mentor = Mentor('Some', 'Buddy')
cool_mentor.courses_attached += ['Python']
 
cool_mentor.rate_hw(best_student, 'Python', 10)
cool_mentor.rate_hw(best_student, 'Python', 10)
cool_mentor.rate_hw(best_student, 'Python', 10)
 
print(best_student.grades)'''


lecturer = Lecturer('Иван', 'Иванов')
reviewer = Reviewer('Пётр', 'Петров')
print(isinstance(lecturer, Mentor)) # True
print(isinstance(reviewer, Mentor)) # True
print(lecturer.courses_attached)    # []
print(reviewer.courses_attached)    # []