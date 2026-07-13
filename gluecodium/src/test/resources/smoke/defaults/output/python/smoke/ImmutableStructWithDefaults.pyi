



from _native_base import _NativeBase

import generated


class ImmutableStructWithDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], ImmutableStructWithDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.ImmutableStructWithDefaults(*args))


    @property
    def int_field(self) -> int:
        """"""
        return self._native.int_field

    @int_field.setter
    def int_field(self, value: int):
        self._native.int_field = value


