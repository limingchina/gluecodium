

from enum import Enum
import typing

class DartExternalCtor:

    field: str

    @staticmethod
    def make(field: str) -> DartExternalCtor:
        ...


