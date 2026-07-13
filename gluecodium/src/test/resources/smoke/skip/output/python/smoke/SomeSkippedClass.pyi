

from dont.smoke.DontSmokeEnum import DontSmokeEnum

from _native_base import _NativeBase


class SomeSkippedClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def do_foo(self) -> DontSmokeEnum:
        """"""
        return self._native.do_foo()

