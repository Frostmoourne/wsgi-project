from wsgi_framework.core import AppClass, DebugApp, MockApp
from wsgi_framework.templates import render
from models import SiteInterface
from logger import Logger, debug

site = SiteInterface()
logger = Logger('Main')


def main_view(request):
    logger.log("Список курсов")
    return '200 OK', render('main.html', objects_list=site.courses)


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
        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))
            course = site.create_course('record', name, category)
            site.courses.append(course)
        return '200 OK', render('create_course.html')
    else:
        categories = site.categories
        return '200 OK', render('create_course.html', categories=categories)


def create_category(request):
    if request['method'] == 'POST':
        data = request['data']
        name = data['name']
        category_id = data.get('category_id')
        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))
        new_category = site.create_category(name, category)
        site.categories.append(new_category)
        return '200 OK', render('create_category.html')
    else:
        categories = site.categories
        return '200 OK', render('create_category.html', categories=categories)


urlpatterns = {
    '/': main_view,
    '/create-category/': create_category,
    '/create-course/': create_course,
    '/contacts/': contacts_view,
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

    return '200 OK', render('main.html', objects_list=site.courses)


@application.add_route('/category-list/')
def category_list(request):
    logger.log('Список категорий')
    return '200 OK', render('category_list.html', objects_list=site.categories)
