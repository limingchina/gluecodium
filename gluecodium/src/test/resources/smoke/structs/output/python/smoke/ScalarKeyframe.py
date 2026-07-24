

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class ScalarKeyframe(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.ScalarKeyframe):
            super().__init__(args[0])
        else:
            super().__init__(generated.ScalarKeyframe(*[_unwrap(arg) for arg in args]))


    @property
    def value(self) -> float:
        """"""
        return _wrap(self._native.value, float)



    @property
    def offset_in_ms(self) -> int:
        """"""
        return _wrap(self._native.offset_in_ms, int)


