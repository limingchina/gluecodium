

from smoke.AsyncErrorCode import AsyncErrorCode
import typing

class AsyncError(Exception):
    message: str

    def __init__(self, message: str) -> None: ...

