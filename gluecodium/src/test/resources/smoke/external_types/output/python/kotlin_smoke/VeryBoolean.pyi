

from enum import Enum
import typing

class VeryBoolean:

    value: bool

    @staticmethod
    def make(value: bool) -> VeryBoolean:
        ...


