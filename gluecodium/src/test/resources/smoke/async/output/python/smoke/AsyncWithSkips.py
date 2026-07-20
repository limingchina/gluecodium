

from __future__ import annotations


from _native_base import _NativeBase

import generated


class AsyncWithSkips(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def make_shared_instance(*args, **kwargs):
        """"""
        generated.AsyncWithSkips.make_shared_instance(*[getattr(a, "_native", a) for a in args])


