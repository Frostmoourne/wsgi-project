from wsgi_framework.templates import render


def main_view(request):
    secret = request.get('secret_key', None)
    return '200 OK', render('index.html', secret=secret)


def about_view(request):
    return '200 OK', render('about.html')


def contacts_view(request):
    return '200 OK', render('contacts.html')
