

from enum import Enum
import typing
from typing import Optional

class WithStringError(Exception):
    message: str

    def __init__(self, message: str) -> None: ...
