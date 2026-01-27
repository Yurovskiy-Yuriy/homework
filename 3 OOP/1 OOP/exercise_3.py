'''Задание № 3. Полиморфизм и магические методы
1) Перегрузите магический метод __str__ у всех классов.
    У проверяющих он должен выводить информацию в следующем виде:
        print(some_reviewer)
        Имя: Some
        Фамилия: Buddy
    
    У лекторов:
        print(some_lecturer)
        Имя: Some
        Фамилия: Buddy
        Средняя оценка за лекции: 9.9
    
    А у студентов так:
        print(some_student)
        Имя: Ruoy
        Фамилия: Eman
        редняя оценка за домашние задания: 9.9
        Курсы в процессе изучения: Python, Git
        Завершенные курсы: Введение в программирование

2) Реализуйте возможность сравнивать (через операторы сравнения)
    между собой лекторов по средней оценке за лекции и студентов
    по средней оценке за домашние задания.'''

class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = [] # список завершенных курсов
        self.courses_in_progress = [] # список курсов студентов
        self.grades = {}   # список оценок студентов 
        
    def __str__(self):
        calculator = AverageGradeCalculator()
        self.avg_grade = calculator.calculator_average_grade(self.grades.values())
        return f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {self.avg_grade}\nКурсы в процессе изучения: {', '.join(self.courses_in_progress)}\nЗавершенные курсы: {', '.join(self.finished_courses)}'

    def __eq__(self, other):
        calculator = AverageGradeCalculator()
        self_avg_grade = calculator.calculator_average_grade(self.grades.values())
        other_avg_grade = calculator.calculator_average_grade(other.grades.values())
        return self_avg_grade == other_avg_grade

    def __lt__(self, other):
        calculator = AverageGradeCalculator()
        self_avg_grade = calculator.calculator_average_grade(self.grades.values())
        other_avg_grade = calculator.calculator_average_grade(other.grades.values())
        return self_avg_grade < other_avg_grade
    
    def __gt__(self, other):
        calculator = AverageGradeCalculator()
        self_avg_grade = calculator.calculator_average_grade(self.grades.values())
        other_avg_grade = calculator.calculator_average_grade(other.grades.values())
        return self_avg_grade > other_avg_grade
               
        
    def rate_lecture(self, lecturer, course, grade): # Студент ставит лектору оценку за лекцию
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades_lect:
                lecturer.grades_lect[course] += [grade] # добавляем оценку к существующему курсу
            else:
                lecturer.grades_lect[course] = [grade] # cсоздаем новый курс и добавляем оценку
            return None
        else:
            return 'Ошибка'        
          
class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = [] #список курсов который преподает лектор
        
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

class Lecturer(Mentor):  # Лектора
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades_lect = {} # список оценок лекторов

    def __str__(self):
        calculator = AverageGradeCalculator()
        self.avg_grade = calculator.calculator_average_grade(self.grades_lect.values())      
        return f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {self.avg_grade}' 

    def __eq__(self, other):
        calculator = AverageGradeCalculator()
        self_avg_grade = calculator.calculator_average_grade(self.grades_lect.values())
        other_avg_grade = calculator.calculator_average_grade(other.grades_lect.values())
        return self_avg_grade == other_avg_grade

    def __lt__(self, other):
        calculator = AverageGradeCalculator()
        self_avg_grade = calculator.calculator_average_grade(self.grades_lect.values())
        other_avg_grade = calculator.calculator_average_grade(other.grades_lect.values())
        return self_avg_grade < other_avg_grade
    
    def __gt__(self, other):
        calculator = AverageGradeCalculator()
        self_avg_grade = calculator.calculator_average_grade(self.grades_lect.values())
        other_avg_grade = calculator.calculator_average_grade(other.grades_lect.values())
        return self_avg_grade > other_avg_grade
               

class Reviewer(Mentor):  # Проверяющие
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'
    
class AverageGradeCalculator:  #Калькулятор расчета средней оценки     
    def calculator_average_grade(self, list_grade):
        list_grades = []
        for x in list_grade:
            list_grades.extend(x)
            if len(list_grades) == 0: # проверка на отуствие оценок
                return None
            else:
                return sum(list_grades) / len(list_grades)


best_student = Student('Роза', 'Смайлова', 'Ж')
best_student.courses_in_progress += ['Python']
 
cool_mentor = Mentor('Some', 'Buddy')
cool_mentor.courses_attached += ['Python']
 
cool_mentor.rate_hw(best_student, 'Python', 10)
cool_mentor.rate_hw(best_student, 'Python', 10)
cool_mentor.rate_hw(best_student, 'Python', 10)
 
lecturer = Lecturer('Иван', 'Иванов')
reviewer = Reviewer('Пётр', 'Петров')
student = Student('Алёхина', 'Ольга', 'Ж')
 
student.courses_in_progress += ['Python', 'Java']
lecturer.courses_attached += ['Python', 'C++']
reviewer.courses_attached += ['Python', 'C++']
 
print(student.rate_lecture(lecturer, 'Python', 7))   # None
print(student.rate_lecture(lecturer, 'Python', 10))   # None
'''print(student.rate_lecture(lecturer, 'Java', 8))     # Ошибка
print(student.rate_lecture(lecturer, 'С++', 8))      # Ошибка
print(student.rate_lecture(reviewer, 'Python', 6))   # Ошибка'''
#print(lecturer.grades_lect)  # {'Python': [7]}  
print()
print('     Магический метод __str__:')
print(reviewer)
print()
print(lecturer)
print()
best_student.finished_courses += ['С++']
print(best_student)
print()
print(student)
print()

        # для операторов сравнения:
print('        Операторы сравнения:\n   Студенты:')
student_2 = Student('Петр', 'Петров', 'М')
student_3 = Student('Антон', 'Антонов', 'М')
student_2.grades['C++'] = [7, 8, 9]
student_3.grades['Python'] = [7, 8, 10]
print(student_2 == student_3)
print(student_2 != student_3)
print(student_2 > student_3)
print(student_2 < student_3)
print('   Лекторы:')
lecturer_2 = Lecturer('Петр', 'Петров')
lecturer_3 = Lecturer('Сергей', 'Сергеев')
lecturer_2.grades_lect['C++'] = [9, 8, 9]
lecturer_3.grades_lect['Python'] = [8, 10, 10]

print(lecturer_2 == lecturer_3)
print(lecturer_2 != lecturer_3)
print(lecturer_2 > lecturer_3)
print(lecturer_2 < lecturer_3)

