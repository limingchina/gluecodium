

from smoke.ClassInStructFooChecker import ClassInStructFooChecker
import typing


from _native_base import _NativeBase

import generated


class ClassInStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.ClassInStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.ClassInStruct(*[_unwrap(arg) for arg in args]))

