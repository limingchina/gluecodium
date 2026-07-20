

from smoke.OuterNameInnerName import OuterNameInnerName
import typing

from _native_base import _NativeBase

import generated


class UseInnerName(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def do_foo(self) -> OuterNameInnerName: ...

