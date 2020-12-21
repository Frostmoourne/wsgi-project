from patterns.prototype import PrototypeMixin
from patterns.observer import Observer, Subject
import jsonpickle


class User:
    def __init__(self, name):
        self.name = name


class Teacher(User):
    pass


class Student(User):
    def __init__(self, name):
        self.courses = []
        super().__init__(name)


class UserFactory:
    types = {'student': Student, 'teacher': Teacher}

    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


class Category:
    pk_id = 0

    def __getitem__(self, item):
        return self.courses[item]

    def __init__(self, name, category):
        self.id = Category.pk_id
        Category.pk_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_number(self):
        res = len(self.courses)
        if self.category:
            res += self.category.course_number()
        return res


class Course(PrototypeMixin, Subject):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


class SmsNotifier(Observer):
    def update(self, subject: Course):
        print(f'SMS: Новый студент {subject.students[-1].name}')


class EmailNotifier(Observer):
    def update(self, subject: Course):
        print(f'EMAIL: Новый студент {subject.students[-1].name}')


class Serializer:
    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return jsonpickle.dumps(self.obj)

    def load(self, data):
        return jsonpickle.loads(data)


class WebinarCourse(Course):
    pass


class RecordCourse(Course):
    pass

class CourseFactory:
    types = {
        'webinar': WebinarCourse,
        'record': RecordCourse
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class SiteInterface:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    def create_user(self, type_, name):
        return UserFactory.create(type_, name)

    def create_category(self, name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for i in self.categories:
            print(i.id)
            if i.id == id:
                return i
        raise Exception(f'Категории id {id} не существует')

    def create_course(self, type_, name, category):
        return CourseFactory.create(type_, name, category)

    def get_course(self, name):
        for course in self.courses:
            if course.name == name:
                return course

    def get_student(self, name):
        for student in self.students:
            if student.name == name:
                return student
