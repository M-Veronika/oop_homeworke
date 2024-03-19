from functools import reduce


class Averageble:
    __nums_arrs = {}

    def set_nums(self, nums):
        self.__nums_arrs = nums

    def get_average(self):
        if not len(self.__nums_arrs):
            return 0

        all_nums = len(self.__nums_arrs) and reduce(lambda x, y: x + y, self.__nums_arrs)
        return sum(all_nums) / len(all_nums)

    def __lt__(self, other):
        if not isinstance(other, Averageble):
            raise NotImplementedError('Не считается')
        return self.get_average() < other.get_average()

    def __gt__(self, other):
        if not isinstance(other, Averageble):
            raise NotImplementedError('Не считается')
        return self.get_average() > other.get_average()

    def __le__(self, other):
        if not isinstance(other, Averageble):
            raise NotImplementedError('Не считается')
        return self.get_average() <= other.get_average()

    def __ge__(self, other):
        if not isinstance(other, Averageble):
            raise NotImplementedError('Не считается')
        return self.get_average() >= other.get_average()

    def __eq__(self, other):
        if not isinstance(other, Averageble):
            raise NotImplementedError('Не считается')
        return self.get_average() == other.get_average()

    def __ne__(self, other):
        if not isinstance(other, Averageble):
            raise NotImplementedError('Не считается')
        return self.get_average() != other.get_average()


class Student(Averageble):
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __str__(self):
        return f'Имя: {self.name}\n' \
               f'Фамилия: {self.surname}\n' \
               f'Средняя оценка за домашние задания: {self.get_average()}\n' \
               f'Курсы в процессе изучения: {self.courses_in_progress}\n' \
               f'Завершенные курсы: {self.finished_courses}\n'

    @staticmethod
    def grade_lecturer(lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and course:
            if course in lecturer.course_grades:
                lecturer.course_grades[course] += [grade]
            else:
                lecturer.course_grades[course] = [grade]
            lecturer.set_nums(lecturer.course_grades.values())
        else:
            return 'Ошибка'


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor, Averageble):
    def __init__(self, name, surname):
        Mentor.__init__(self, name, surname)
        self.course_grades = {}

    def __str__(self):
        return f'Имя: {self.name}\n' \
               f'Фамилия: {self.surname}\n' \
               f'Средняя оценка за лекции: {self.get_average()}\n'


class Reviewer(Mentor):
    def __init__(self, name, surname):
        Mentor.__init__(self, name, surname)

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}\n'

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
            student.set_nums(student.grades.values())
        else:
            return 'Ошибка'


def get_students_average(students_list: list, course_name: str):
    nums_for_average = [
        student.grades[course_name]
        for student in students_list
        if isinstance(student, Student) and course_name in student.grades
    ]
    average = Averageble()
    average.set_nums(nums_for_average)
    return average.get_average()


def get_lecturer_average(lecturer_list: list, course_name: str):
    nums_for_average = [
        lecturer.course_grades[course_name]
        for lecturer in lecturer_list
        if isinstance(lecturer, Lecturer) and course_name in lecturer.course_grades
    ]
    average = Averageble()
    average.set_nums(nums_for_average)
    return average.get_average()


best_student = Student('Student', 'A', 'your_gender')
best_student.courses_in_progress += ['Python']

best_student2 = Student('Student2', 'B', 'your_gender')
best_student2.courses_in_progress += ['Python']

cool_reviewer = Reviewer('Reviewer', 'A')
cool_reviewer.courses_attached += ['Python']

cool_reviewer2 = Reviewer('Reviewer2', 'B')
cool_reviewer2.courses_attached += ['Python']

cool_lecturer = Lecturer('Lecturer', 'A')
cool_lecturer.courses_attached += ['Python']

cool_lecturer2 = Lecturer('Lecturer2', 'B')
cool_lecturer2.courses_attached += ['Python']

cool_reviewer.rate_hw(best_student, 'Python', 4)
cool_reviewer.rate_hw(best_student, 'Python', 6)
cool_reviewer2.rate_hw(best_student, 'Python', 10)

best_student.grade_lecturer(cool_lecturer, 'Python', 10)
best_student.grade_lecturer(cool_lecturer, 'Python', 2)
best_student.grade_lecturer(cool_lecturer2, 'Python', 7)

print(best_student)
print(cool_lecturer)
print(best_student > cool_lecturer)
print(best_student >= cool_lecturer2)
print(best_student2 == cool_lecturer2)

print(cool_lecturer.course_grades)

print(get_students_average([best_student, best_student2], 'Python'))
print(get_lecturer_average([cool_lecturer2, cool_lecturer], 'Python'))
