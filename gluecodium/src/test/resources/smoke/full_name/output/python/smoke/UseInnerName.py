

from __future__ import annotations

from smoke.OuterNameInnerName import OuterNameInnerName


from _native_base import _NativeBase

import generated


class UseInnerName(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def do_foo(self) -> OuterNameInnerName:
        """"""
        return self._native.do_foo()

