'''Задание № 2. Атрибуты и взаимодействие классов.
В квизе к предыдущей лекции мы реализовали возможность
выставлять студентам оценки за домашние задания. Теперь
это могут делать только Reviewer (реализуйте такой метод)!
А что могут делать лекторы? Получать оценки за лекции от 
студентов :) Реализуйте метод выставления оценок лекторам
у класса Student (оценки по 10-балльной шкале, хранятся в
атрибуте-словаре у Lecturer, в котором ключи – названия
курсов, а значения – списки оценок). Лектор при этом должен
быть закреплен за тем курсом, на который записан студент.'''

class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

# Начало выполнения домашнего задания: 
    def rate_lecture(self, lecturer, course, grade): # Студент ставит лектору оценку за лекцию
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade] # добавляем оценку к существующему курсу
            else:
                lecturer.grades[course] = [grade] # cсоздаем новый курс и добавляем оценку
            return None
        else:
            return 'Ошибка'        
# Конец выполнения домашнего задания. 
          
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

class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}       # добавлено при выполнении домашнего задания. 

class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

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
student = Student('Алёхина', 'Ольга', 'Ж')
 
student.courses_in_progress += ['Python', 'Java']
lecturer.courses_attached += ['Python', 'C++']
reviewer.courses_attached += ['Python', 'C++']
 
print(student.rate_lecture(lecturer, 'Python', 7))   # None
print(student.rate_lecture(lecturer, 'Java', 8))     # Ошибка
print(student.rate_lecture(lecturer, 'С++', 8))      # Ошибка
print(student.rate_lecture(reviewer, 'Python', 6))   # Ошибка

print(lecturer.grades)  # {'Python': [7]}  