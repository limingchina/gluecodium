

from __future__ import annotations



from _native_base import _NativeBase

import generated


class ScalarKeyframe(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.ScalarKeyframe):
            super().__init__(args[0])
        else:
            super().__init__(generated.ScalarKeyframe(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def value(self) -> float:
        """"""
        return self._native.value



    @property
    def offset_in_ms(self) -> int:
        """"""
        return self._native.offset_in_ms


