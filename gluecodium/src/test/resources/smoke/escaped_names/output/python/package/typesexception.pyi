

from package.typesenum import typesenum
import typing

class typesexception(Exception):
    message: str

    def __init__(self, message: str) -> None: ...

