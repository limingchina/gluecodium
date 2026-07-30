

from smoke.OuterStructInnerEnum import OuterStructInnerEnum
import typing

class OuterStructInstantiation(Exception):
    message: str

    def __init__(self, message: str) -> None: ...

