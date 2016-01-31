from functools import wraps


def requires_authentication(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # TODO
        return f(*args, **kwargs)
    return decorated_function


def requires_superuser(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # TODO
        return f(*args, **kwargs)
    return decorated_function
