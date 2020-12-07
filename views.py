from wsgi_framework.templates import render


def main_view(request):
    secret = request.get('secret_key', None)
    return '200 OK', render('index.html', secret=secret)


def about_view(request):
    return '200 OK', render('about.html')


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

