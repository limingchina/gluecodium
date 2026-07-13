



from _native_base import _NativeBase

import generated


class TimeZone(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], TimeZone):
            super().__init__(args[0])
        else:
            super().__init__(generated.TimeZone(*args))


    @property
    def raw_offset(self) -> int:
        """"""
        return self._native.raw_offset

    @raw_offset.setter
    def raw_offset(self, value: int):
        self._native.raw_offset = value


