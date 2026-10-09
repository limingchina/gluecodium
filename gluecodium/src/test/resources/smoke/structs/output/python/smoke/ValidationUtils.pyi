

from enum import Enum
import typing
from typing import Optional

class ValidationUtils:
    def __init__(self) -> None: ...

    class ValidationErrorCode(Enum):

        NONE = 0
        VALIDATION_FAILED = 1



    class ValidationError(Exception):
        message: str

        def __init__(self, message: str) -> None: ...
