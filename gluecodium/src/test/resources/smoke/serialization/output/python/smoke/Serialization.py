

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.SerializationNestedSerializableStruct import SerializationNestedSerializableStruct
from smoke.SerializationSomeEnum import SerializationSomeEnum


from _native_base import _NativeBase

import generated


class Serialization(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_Serialization):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_Serialization(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

