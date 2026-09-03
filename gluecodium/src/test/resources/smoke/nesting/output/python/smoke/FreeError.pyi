

from smoke.FreeEnum import FreeEnum
from enum import Enum
import typing

class FreeError(Exception):
    message: str

    def __init__(self, message: str) -> None: ...


