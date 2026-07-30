

from smoke.Payload import Payload
import typing

class WithPayloadError(Exception):
    message: str

    def __init__(self, message: str) -> None: ...

