

from smoke.FreeEnum import FreeEnum
import typing

class FreeError(Exception):
    message: str

    def __init__(self, message: str) -> None: ...

