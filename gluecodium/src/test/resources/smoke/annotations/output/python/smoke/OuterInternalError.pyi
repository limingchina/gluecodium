

from smoke.OuterInternalEnum import OuterInternalEnum
import typing

class OuterInternalError(Exception):
    """"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

