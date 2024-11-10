from functools import wraps


def decorate_replacement_identifier(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)

        if (
            self.application.application_permit_type == "replacement"
            and result is not None
        ):
            return f"RP-{result}"
        return result

    return wrapper
