

from dont.smoke.DontSmokeEnum import DontSmokeEnum

from _native_base import _NativeBase


class SkippedFunctionClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def do_foo(self, input: DontSmokeEnum):
        """"""
        return self._native.do_foo(input)

