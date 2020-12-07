class AppClass:

    def __init__(self, urlpatterns: dict, front_controllers: list):
        """
        :param urlpatterns:
        :param front_controllers:
        """
        self.urlpatterns = urlpatterns
        self.front_controllers = front_controllers

    def __call__(self, env, start_response):
        path = env['PATH_INFO']
        if path[-1] != '/':
            path = path + '/'
        if path in self.urlpatterns:
            view = self.urlpatterns[path]
            request = {}

            for controller in self.front_controllers:
                controller(request)

            code, text = view(request)
            start_response(code, [('Content-Type', 'text/html')])
            return [text.encode('utf-8')]
        else:
            start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
            return [b'Not Found']
