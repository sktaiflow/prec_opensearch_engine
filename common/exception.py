from typing import Optional, Union

class OpensearchError(Exception):
    def __init__(
        self,
        api: str,
        status_code: Optional[int] = None,
        code: Optional[str] = None,
        message: Optional[Union[str, dict]] = None,
    ) -> None:
        error_message = f"Error requesting {api}"
        if status_code:
            error_message += f". Status code: {status_code}"
        if code:
            error_message += f". Code: {code}"
        if message:
            error_message += f". Message: {message}"
        super().__init__(error_message)
        self.api = api
        self.status_code = status_code
        self.code = code
        self.message = error_message