from functools import wraps


def decorate_renewal_identifier(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)

        if self.application.application_permit_type == 'renewal' and result is not None:
            return f"RW/{result}"
        return result
    return wrapper
