

from enum import Enum
import typing
from typing import Optional

class AttributesCrashError(Exception):
    message: str

    def __init__(self, message: str) -> None: ...
