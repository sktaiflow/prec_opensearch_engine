from typing import Callable
from functools import wraps
from utils.enum import INTERNAL_ERROR_CODES


def exception_handle_operation(error_code: INTERNAL_ERROR_CODES):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                response = func(*args, **kwargs)
                code = INTERNAL_ERROR_CODES.SUCCESS
                message = INTERNAL_ERROR_CODES.get_message(code)
            except Exception as e:
                code = error_code.value
                message = INTERNAL_ERROR_CODES.get_message(code, e)
                response = None
            finally:
                return {"response": response, "code": code, "message": message}
        return wrapper
    return decorator