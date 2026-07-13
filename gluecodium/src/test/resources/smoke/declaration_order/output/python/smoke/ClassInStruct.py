

from __future__ import annotations

from smoke.FooChecker import FooChecker


from _native_base import _NativeBase

import generated


class ClassInStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], ClassInStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.ClassInStruct(*args))

