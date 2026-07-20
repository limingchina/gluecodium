

from smoke.AsyncErrorCode import AsyncErrorCode
import typing

class AsyncError(Exception):
    """"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

