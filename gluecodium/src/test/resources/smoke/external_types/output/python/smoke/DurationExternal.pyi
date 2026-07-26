

import typing


from _native_base import _NativeBase

import generated


class DurationExternal(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_DurationExternal):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_DurationExternal(*[_unwrap(arg) for arg in args]))


    @property
    def value(self) -> int:
        """"""
        return _wrap(self._native.value, int)


