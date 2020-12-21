from wsgi_framework.core import AppClass, DebugApp, MockApp
from wsgi_framework.frameworkcbv import CreateView, ListView
from wsgi_framework.templates import render
from models import SiteInterface, EmailNotifier, SmsNotifier, Serializer
from logger import Logger, debug

site = SiteInterface()
logger = Logger('Main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()


def main_view(request):
    logger.log("Список курсов")
    return '200 OK', render('course_list.html', objects_list=site.courses)


def contacts_view(request):
    if request['method'] == 'POST':
        data = request['data']
        title = data['title']
        email = data['email']
        text = data['text']
        with open(f'{email} - {title}.txt', 'w', encoding='utf-8') as f:
            f.write(text)
        return '200 OK', render('contacts.html')
    else:
        return '200 OK', render('contacts.html')


@debug
def create_course(request):
    if request['method'] == 'POST':
        data = request['data']
        name = data['name']
        category_id = data.get('category_id')
        if category_id:
            category = site.find_category_by_id(int(category_id))
            course = site.create_course('record', name, category)
            course.observers.append(email_notifier)
            course.observers.append(sms_notifier)
            site.courses.append(course)
        categories = site.categories
        return '200 OK', render('create_course.html', categories=categories)
    else:
        categories = site.categories
        return '200 OK', render('create_course.html', categories=categories)


class CategoryCreateView(CreateView):
    template_name = 'create_category.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['categories'] = site.categories
        return context

    def create_object(self, data):
        name = data['name']
        category_id = data.get('category_id')

        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))

        new_category = site.create_category(name, category)
        site.categories.append(new_category)


# def create_category(request):
#     if request['method'] == 'POST':
#         data = request['data']
#         name = data['name']
#         category_id = data.get('category_id')
#         category = None
#         if category_id:
#             category = site.find_category_by_id(int(category_id))
#         new_category = site.create_category(name, category)
#         site.categories.append(new_category)
#         return '200 OK', render('create_category.html')
#     else:
#         categories = site.categories
#         return '200 OK', render('create_category.html', categories=categories)


class CategoryListView(ListView):
    queryset = site.categories
    template_name = 'category_list.html'


class StudentsListView(ListView):
    queryset = site.students
    template_name = 'students_list.html'


class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_object(self, data):
        name = data['name']
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)


class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_object(self, data):
        print(data)
        course_name = data['course_name']
        course = site.get_course(course_name)
        student_name = data['student_name']
        student = site.get_student(student_name)
        course.add_student(student)


urlpatterns = {
    '/': main_view,
    '/create-category/': CategoryCreateView(),
    '/create-course/': create_course,
    '/contacts/': contacts_view,
    '/category-list/': CategoryListView(),
    '/students-list/': StudentsListView(),
    '/create-student/': StudentCreateView(),
    '/add-student/': AddStudentByCourseCreateView(),
}


def secret_controller(request):
    request['secret_key'] = 'SECRET KEY'


front_controllers = [
    secret_controller
]

application = AppClass(urlpatterns, front_controllers)


@application.add_route('/copy-course/')
def copy_course(request):
    request_parameters = request['request_params']
    name = request_parameters['name']
    old_course = site.get_course(name)
    if old_course:
        new_name = f'copy_{name}'
        new_course = old_course.clone()
        new_course.name = new_name
        site.courses.append(new_course)

    return '200 OK', render('course_list.html', objects_list=site.courses)


# @application.add_route('/category-list/')
# def category_list(request):
#     logger.log('Список категорий')
#     return '200 OK', render('category_list.html', objects_list=site.categories)

@application.add_route('/api/')
def course_api(request):
    return '200 OK', Serializer(site.courses).save()
