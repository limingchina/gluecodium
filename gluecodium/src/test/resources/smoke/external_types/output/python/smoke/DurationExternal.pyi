



from _native_base import _NativeBase

import generated


class DurationExternal(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], DurationExternal):
            super().__init__(args[0])
        else:
            super().__init__(generated.DurationExternal(*args))


    @property
    def value(self) -> int:
        """"""
        return self._native.value

    @value.setter
    def value(self, value: int):
        self._native.value = value


