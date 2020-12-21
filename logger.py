from patterns.singletone import Singleton
import time


class ConsoleOutput:
    def write(self, text):
        print(text)


class FileOutput:

    def __init__(self, file_name):
        self.file_name = file_name

    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')


class Logger(metaclass=Singleton):
    def __init__(self, name, writer=ConsoleOutput()):
        self.name = name
        self.writer = writer

    def log(self, text):
        print("log:  ", text)
        self.writer.write(text)


def debug(func):
    def inner(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        print("DEBUG:   ", func.__name__, end - start)
        return res
    return inner
