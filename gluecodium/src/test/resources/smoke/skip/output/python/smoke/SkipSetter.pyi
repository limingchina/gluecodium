

from enum import Enum
import typing
from typing import Optional

class SkipSetter:

    @property
    def foo(self) -> str:
        ...
