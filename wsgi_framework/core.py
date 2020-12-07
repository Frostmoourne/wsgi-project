class AppClass:

    def parse_in_data(self, data: str):
        """
        Функция разбора строки браузера на отдельные параметры
        :param data:
        :return:
        """
        result = {}
        if data:
            parameters = data.split('&')
            for param in parameters:
                i, j = param.split('=')
                result[i] = j
        return result

    def parse_wsgi_in_data(self, data: bytes):
        """
        Функция декодирования входящих параметров из строки браузера
        :param data:
        :return:
        """
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = self.parse_in_data(data_str)
        return result

    def get_wsgi_in_data(self, environ):
        content_len_data = environ.get('CONTENT_LENGTH')
        content_len = int(content_len_data) if content_len_data else 0
        data = environ['wsgi.input'].read(content_len) if content_len > 0 else b''
        return data

    def __init__(self, urlpatterns: dict, front_controllers: list):
        """
        :param urlpatterns:
        :param front_controllers:
        """
        self.urlpatterns = urlpatterns
        self.front_controllers = front_controllers

    def __call__(self, env, start_response):
        path = env['PATH_INFO']
        if not path.endswith('/'):
            path = f'{path}/'

        method = env['REQUEST_METHOD']
        data = self.get_wsgi_in_data(env)
        data = self.parse_wsgi_in_data(data)

        query_string = env['QUERY_STRING']
        request_parameters = self.parse_in_data(query_string)

        if path in self.urlpatterns:
            view = self.urlpatterns[path]
            request = {'method': method, 'data': data, 'request_params': request_parameters}

            for controller in self.front_controllers:
                controller(request)

            code, text = view(request)
            start_response(code, [('Content-Type', 'text/html')])
            return [text.encode('utf-8')]
        else:
            start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
            return [b'Not Found']
