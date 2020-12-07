from jinja2 import Template
import os


def render(template_name, folder='templates', **kwargs):
    """
    Фунция рендерит шаблон шаблона с входящими параметрами
    :param template_name:
    :param folder:
    :param kwargs:
    :return:
    """
    path = os.path.join(folder, template_name)

    with open(path, encoding='utf-8') as file:
        template = Template(file.read())

    return template.render(**kwargs)
