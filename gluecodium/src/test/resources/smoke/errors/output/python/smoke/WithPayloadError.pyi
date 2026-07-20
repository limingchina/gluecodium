

from smoke.Payload import Payload
import typing

class WithPayloadError(Exception):
    """"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

