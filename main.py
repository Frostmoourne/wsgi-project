from wsgi_framework.core import AppClass
import views


urlpatterns = {
    '/': views.main_view,
    '/about/': views.about_view,
    '/contacts/': views.contacts_view,
}


def secret_controller(request):
    request['secret_key'] = 'SECRET KEY'


front_controllers = [
    secret_controller
]

application = AppClass(urlpatterns, front_controllers)
