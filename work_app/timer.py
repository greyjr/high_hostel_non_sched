from datetime import datetime


def timer(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        end = datetime.now()
        print('function: ', func.__repr__(), 'duration: ', end - start)
        return result
    return wrapper

