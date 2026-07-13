

from smoke.NestedEquatableStruct import NestedEquatableStruct
from smoke.SomeEnum import SomeEnum
from smoke.dict[int, str] import dict[int, str]


from _native_base import _NativeBase

import generated


class Equatable(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], Equatable):
            super().__init__(args[0])
        else:
            super().__init__(generated.Equatable(*args))

