

from dont.smoke.DontSmokeEnum import DontSmokeEnum
import typing

from _native_base import _NativeBase

import generated


class SkippedFunctionClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def do_foo(self, input: DontSmokeEnum): ...

