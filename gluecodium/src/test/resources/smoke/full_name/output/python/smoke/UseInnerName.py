

from __future__ import annotations

from smoke.InnerName import InnerName


from _native_base import _NativeBase

import generated


class UseInnerName(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def do_foo(self) -> InnerName:
        """"""
        return self._native.do_foo()

