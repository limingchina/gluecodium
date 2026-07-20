

from smoke.SomeInternalEnum import SomeInternalEnum
import typing

class SomethingBadHappenedError(Exception):
    """"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

