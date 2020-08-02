# заглушка - проверка авторизирован ли работник хостела


def is_login_manager(func):
    def wrapper(*args, **kwargs):
        pass
        result = func(*args, **kwargs)
        return result
    return wrapper
