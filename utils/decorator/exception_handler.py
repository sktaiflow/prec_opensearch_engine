from typing import Callable
from functools import wraps


def exception_handle_operation(error_code: InternalCodes):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                response = func(*args, **kwargs)
                code = InternalCodes.SUCCESS.value
                message = InternalCodes.get_message(code)
            except Exception as e:
                code = error_code.value
                message = InternalCodes.get_message(code, e)
                response = None
            finally:
                return {"response": response, "code": code, "message": message}
        return wrapper
    return decorator