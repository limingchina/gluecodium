

from smoke.Payload import Payload
from enum import Enum
import typing

class WithPayloadError(Exception):
    message: str

    def __init__(self, message: str) -> None: ...


