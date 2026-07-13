



from _native_base import _NativeBase

import generated


class SerializableEquatableStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], SerializableEquatableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.SerializableEquatableStruct(*args))


    @property
    def foo_field(self) -> str:
        """"""
        return self._native.foo_field

    @foo_field.setter
    def foo_field(self, value: str):
        self._native.foo_field = value


