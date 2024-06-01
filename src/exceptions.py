from werkzeug.exceptions import HTTPException


class UnicornException(HTTPException):
    def __init__(self, result: bool, error_type: str, error_message: str):
        self.result: bool = result
        self.error_type: str = error_type
        self.error_message: str = error_message
        self.code = 418
        super().__init__(self.error_message)
