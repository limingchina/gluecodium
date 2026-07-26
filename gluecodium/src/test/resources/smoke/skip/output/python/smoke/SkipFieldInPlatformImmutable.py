

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class SkipFieldInPlatformImmutable(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_SkipFieldInPlatformImmutable):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_SkipFieldInPlatformImmutable(*[_unwrap(arg) for arg in args]))


    @property
    def int_field(self) -> int:
        """"""
        return _wrap(self._native.int_field, int)



    @property
    def bool_field(self) -> bool:
        """"""
        return _wrap(self._native.bool_field, bool)


