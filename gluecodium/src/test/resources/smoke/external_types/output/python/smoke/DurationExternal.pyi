

import typing


from _native_base import _NativeBase

import generated


class DurationExternal(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.DurationExternal):
            super().__init__(args[0])
        else:
            super().__init__(generated.DurationExternal(*[_unwrap(arg) for arg in args]))


    @property
    def value(self) -> int:
        """"""
        return _wrap(self._native.value, int)


