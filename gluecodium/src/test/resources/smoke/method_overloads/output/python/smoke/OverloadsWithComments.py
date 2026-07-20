

from __future__ import annotations


from _native_base import _NativeBase

import generated


class OverloadsWithComments(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def do_stuff(*args, **kwargs):
        """"""
        return self._native.do_stuff(*[getattr(a, "_native", a) for a in args])


