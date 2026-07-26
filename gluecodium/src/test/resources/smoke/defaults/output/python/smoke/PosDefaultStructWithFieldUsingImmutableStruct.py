

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.ImmutableStructWithDefaults import ImmutableStructWithDefaults


from _native_base import _NativeBase

import generated


class PosDefaultStructWithFieldUsingImmutableStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_PosDefaultStructWithFieldUsingImmutableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_PosDefaultStructWithFieldUsingImmutableStruct(*[_unwrap(arg) for arg in args]))


    @property
    def some_field1(self) -> ImmutableStructWithDefaults:
        """"""
        return _wrap(self._native.some_field1, ImmutableStructWithDefaults)


