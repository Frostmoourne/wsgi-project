from patterns.singletone import Singleton
import time


class Logger(metaclass=Singleton):
    def __init__(self, name):
        self.name = name

    def log(self, text):
        print("log:  ", text)


def debug(func):
    def inner(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        print("DEBUG:   ", func.__name__, end - start)
        return res
    return inner
