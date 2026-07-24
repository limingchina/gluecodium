

from smoke.SkipTypesNotInDart import SkipTypesNotInDart
import typing

from _native_base import _NativeBase

import generated


class SkipTypes(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def use_list_in_dart(self) -> list[SkipTypesNotInDart]: ...

