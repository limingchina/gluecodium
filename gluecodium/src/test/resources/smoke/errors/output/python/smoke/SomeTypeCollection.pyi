

from enum import Enum
import typing
from typing import Optional

class SomeTypeCollection:

    class SomeTypeCollectionError(Enum):

        ERROR_A = 0
        ERROR_B = 1



    class SomeError(Exception):
        message: str

        def __init__(self, message: str) -> None: ...
