

from smoke.SerializationNestedSerializableStruct import SerializationNestedSerializableStruct
from smoke.SerializationSomeEnum import SerializationSomeEnum
import typing


from _native_base import _NativeBase

import generated


class Serialization(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_Serialization):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_Serialization(*[_unwrap(arg) for arg in args]))

