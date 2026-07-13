

from __future__ import annotations



from _native_base import _NativeBase

import generated


class SpecialAttributes(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def with_escaping(self):
        """"""
        return self._native.with_escaping()


    def with_line_break(self):
        """"""
        return self._native.with_line_break()

