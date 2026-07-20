

from smoke.Basic import Basic
import typing

from _native_base import _NativeBase

import generated


class BasicForwardDeclarations(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def use_basic(self) -> Basic: ...

