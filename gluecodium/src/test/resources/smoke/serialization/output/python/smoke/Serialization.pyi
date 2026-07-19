

from smoke.SerializationNestedSerializableStruct import SerializationNestedSerializableStruct
from smoke.SerializationSomeEnum import SerializationSomeEnum


from _native_base import _NativeBase

import generated


class Serialization(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.Serialization):
            super().__init__(args[0])
        else:
            super().__init__(generated.Serialization(*[getattr(arg, "_native", arg) for arg in args]))

