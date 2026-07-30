

from smoke.ErrorsInternalErrorCode import ErrorsInternalErrorCode
import typing

class ErrorsInternal(Exception):
    message: str

    def __init__(self, message: str) -> None: ...

