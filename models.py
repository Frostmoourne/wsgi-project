from patterns.prototype import PrototypeMixin


class Category:
    pk_id = 0

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


class Course(PrototypeMixin):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


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

    def create_user(self):
        pass

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
        return None
