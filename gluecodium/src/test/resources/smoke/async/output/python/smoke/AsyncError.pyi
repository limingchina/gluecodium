

from smoke.AsyncErrorCode import AsyncErrorCode
from enum import Enum
import typing
from typing import Optional

class AsyncError(Exception):
    message: str

    def __init__(self, message: str) -> None: ...
