'''Задание № 4. Полевые испытания
Создайте по 2 экземпляра каждого класса, вызовите все созданные методы,
а также реализуйте две функции:
    1.	для подсчета средней оценки за домашние задания по всем студентам в
        рамках конкретного курса (в качестве аргументов принимаем список студентов
        и название курса);
    2.	для подсчета средней оценки за лекции всех лекторов в рамках курса (в 
        качестве аргумента принимаем список лекторов и название курса).'''

class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = [] # список завершенных курсов
        self.courses_in_progress = [] # список курсов студентов
        self.grades = {}   # список оценок студентов 
          
    def __str__(self):
        calculator = AverageRating()
        self.avg_grade = calculator.average_rating(self.grades)
        return f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {"{:.1f}".format(self.avg_grade)}\nКурсы в процессе изучения: {', '.join(self.courses_in_progress)}\nЗавершенные курсы: {', '.join(self.finished_courses)}'

    def __eq__(self, other):          
        calculator = AverageRating()
        self_avg_grade = calculator.average_rating(self.grades)
        other_avg_grade = calculator.average_rating(other.grades)
        print(f'{"{:.1f}".format(self_avg_grade)} = {"{:.1f}".format(other_avg_grade)}:')
        return self_avg_grade == other_avg_grade

    def __lt__(self, other):  
        calculator = AverageRating()
        self_avg_grade = calculator.average_rating(self.grades)
        other_avg_grade = calculator.average_rating(other.grades)
        print(f'{"{:.1f}".format(self_avg_grade)} < {"{:.1f}".format(other_avg_grade)}:')
        return self_avg_grade < other_avg_grade
    
    def __gt__(self, other): 
        calculator = AverageRating()
        self_avg_grade = calculator.average_rating(self.grades)
        other_avg_grade = calculator.average_rating(other.grades)
        print(f'{"{:.1f}".format(self_avg_grade)} > {"{:.1f}".format(other_avg_grade)}:')
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
         
    def average_course_rating(self, course, name, surname): #расчет средней оценки за каждый курс
        for key, value in course.items():
            if value == 0:  # проверка на отуствие оценок
                print(None)
            else:               
                grade = sum(value) / len(value)
                print(f'Студент: {name} {surname}. Курс: {key}. Cредняя оценка: {"{:.1f}".format(grade)}') 

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

    def average_course_rating(self, course, name, surname): #расчет средней оценки за каждый курс
        for key, value in course.items():
            if value == 0:  # проверка на отуствие оценок
                print(None)
            else:               
                grade = sum(value) / len(value)
                print(f'Преподаватель: {name} {surname}. Курс: {key}. Cредняя оценка: {"{:.1f}".format(grade)}') 

class Lecturer(Mentor):  # Лектора
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades_lect = {} # список оценок лекторов


    def __str__(self):
        calculator = AverageRating()  
        self.avg_grade = calculator.average_rating(self.grades_lect)      
        return f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {self.avg_grade}' 

    def __eq__(self, other):
        calculator = AverageRating()   
        self_avg_grade = calculator.average_rating(self.grades_lect)
        other_avg_grade = calculator.average_rating(other.grades_lect)
        print(f'{"{:.1f}".format(self_avg_grade)} = {"{:.1f}".format(other_avg_grade)}:')
        return self_avg_grade == other_avg_grade

    def __lt__(self, other):
        calculator = AverageRating()   
        self_avg_grade = calculator.average_rating(self.grades_lect)
        other_avg_grade = calculator.average_rating(other.grades_lect)
        print(f'{"{:.1f}".format(self_avg_grade)} < {"{:.1f}".format(other_avg_grade)}:')
        return self_avg_grade < other_avg_grade
    
    def __gt__(self, other):
        calculator = AverageRating()   
        self_avg_grade = calculator.average_rating(self.grades_lect)
        other_avg_grade = calculator.average_rating(other.grades_lect)
        print(f'{"{:.1f}".format(self_avg_grade)} > {"{:.1f}".format(other_avg_grade)}:')
        return self_avg_grade > other_avg_grade
               

class Reviewer(Mentor):  # Проверяющие
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'

class AverageRating:       #расчет средней оценки учитывая все курсы
    def average_rating(self, course): 
        n = 0
        overall_rating = 0
        for key, value in course.items():
            if value == 0:  # проверка на отуствие оценок
                print(None)
            else:               
                grade = sum(value) / len(value)
                n += 1
                overall_rating += grade
        return overall_rating / n


def average_hw_by_course(students, course_name): # расчет средней оценки студентов по отдельному курсу 
    all_grades = []
    for student in students:
        all_grades.extend(student.grades[course_name]) 
        result = (sum(all_grades) / len(all_grades))
        return print(f'Курс {course_name}: {"{:.1f}".format(result)}')

def average_lectures_by_course(lecturers, course_name): # расчет средней оценки лекторов по отдельному курсу 
    all_grades = []
    for lecturer in lecturers:
        all_grades.extend(lecturer.grades_lect[course_name]) 
        result = sum(all_grades) / len(all_grades)
        return print(f'Курс {course_name}: {"{:.1f}".format(result)}')

student1 = Student('Иван', 'Иванов', 'M')
student2 = Student('Мария', 'Маринова', 'Ж')
lecturer1 = Lecturer('Петр', 'Петров') 
lecturer2 = Lecturer('Сергей', 'Сергеев')
reviewer1 = Reviewer('Антон', 'Антонов')
reviewer2 = Reviewer('Василий', 'Васин')

# Добавляем курсы студентам
student1.courses_in_progress.append('Python')
student2.courses_in_progress.append('Python')
student1.courses_in_progress.append('C++')
student2.courses_in_progress.append('C++')

# Добавляем завершонные курсы студентам 
student1.finished_courses.append('Python')
student2.finished_courses.append('C++')

# Присваиваем курсы преподавателям
lecturer1.courses_attached.append('Python')
lecturer2.courses_attached.append('Python')
lecturer1.courses_attached.append('C++')

# Ставим оценки студентам
student1.grades['Python'] = [7, 8, 9]
student2.grades['Python'] = [7, 8, 10]
student1.grades['C++'] = [5, 8, 9]
student2.grades['C++'] = [7, 6, 10]

# Ставим оценки преподавателям за лекции (ставят студенты)
student1.rate_lecture(lecturer1, 'Python', 8)
student2.rate_lecture(lecturer1, 'Python', 9)
student1.rate_lecture(lecturer2, 'Python', 5)
student2.rate_lecture(lecturer2, 'Python', 9)
student2.rate_lecture(lecturer2, 'C++', 6)     # оценку не смогут поставить, т.к. лектор данный курс не преподает 
student1.rate_lecture(lecturer1, 'C++', 10)
student2.rate_lecture(lecturer1, 'C++', 9)

#магический метод __str__ 
print('     Магический метод __str_:')
print(student1)
print()
print(student2)
print()
print(lecturer1)
print()
print(lecturer2)
print()

# расчет средних оценок по каждому курсу:
print('     Расчет средних оценок студентов по каждому курсу:')
student1.average_course_rating(student1.grades, student1.name, student1.surname)
print()
student2.average_course_rating(student2.grades, student2.name, student2.surname)
print()
print('     Расчет средних оценок лекторов по каждому курсу:')
lecturer1.average_course_rating(lecturer1.grades_lect, lecturer1.name, lecturer1.surname)
print()
lecturer2.average_course_rating(lecturer2.grades_lect, lecturer2.name, lecturer2.surname)
print()

# для операторов сравнения:
print('          Операторы сравнения:\n(сравнение средней оценки за все курсы)\n   Студенты:')
print(student1 == student2)
print(student1 > student2)
print(student1 < student2)
print()
print('   Лекторы:')
print(lecturer1 == lecturer2)
print(lecturer1 > lecturer2)
print(lecturer1 < lecturer2)
print()

# расчет средних оценок за всех студентов по каждому курсу:
students_list = [student1, student2]
lecturers_list = [lecturer1, lecturer2]
print("Средние оценки всех студентов за каждый курс:")
average_hw_by_course(students_list, 'Python')
average_hw_by_course(students_list, 'C++')
print()

# расчет средних оценок за всех лекторов по каждому курсу:
print("Средние оценки всех лекторов за каждый курс:")
average_lectures_by_course(lecturers_list, 'Python')
average_lectures_by_course(lecturers_list, 'C++')
























'''
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
print(student.rate_lecture(lecturer, 'Java', 8))     # Ошибка
print(student.rate_lecture(lecturer, 'С++', 8))      # Ошибка
print(student.rate_lecture(reviewer, 'Python', 6))   # Ошибка
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
print('   Лектора:')
lecturer_2 = Lecturer('Петр', 'Петров')
lecturer_3 = Lecturer('Сергей', 'Сергеев')
lecturer_2.grades_lect['C++'] = [9, 8, 9]
lecturer_3.grades_lect['Python'] = [8, 10, 10]

print(lecturer_2 == lecturer_3)
print(lecturer_2 != lecturer_3)
print(lecturer_2 > lecturer_3)
print(lecturer_2 < lecturer_3)


Задание №4 (Полевые испытания):
•	Созданы по 2 экземпляра каждого класса.
•	Проверены все методы (включая новые).
•	Реализованы 2 функции:
o	Подсчет средней оценки студентов по курсу.
o	Подсчет средней оценки лекторов по курсу.
'''
