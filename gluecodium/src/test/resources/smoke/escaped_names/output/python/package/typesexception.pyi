

from package.typesenum import typesenum
import typing

class typesexception(Exception):
    """"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

