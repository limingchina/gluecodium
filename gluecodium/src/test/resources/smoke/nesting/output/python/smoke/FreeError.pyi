

from smoke.FreeEnum import FreeEnum
import typing

class FreeError(Exception):
    """"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

