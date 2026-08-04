

from enum import Enum
import typing

class PublicStructWithInternalConstructors:

    some_var: int

    @staticmethod
    def _make() -> PublicStructWithInternalConstructors:
        ...


