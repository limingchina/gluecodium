

from smoke.EquatableNestedEquatableStruct import EquatableNestedEquatableStruct
from smoke.EquatableSomeEnum import EquatableSomeEnum
import typing


from _native_base import _NativeBase

import generated


class Equatable(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.Equatable):
            super().__init__(args[0])
        else:
            super().__init__(generated.Equatable(*[getattr(arg, "_native", arg) for arg in args]))

