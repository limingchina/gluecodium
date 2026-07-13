



from _native_base import _NativeBase

import generated


class ExternalInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, ExternalInterface):
            super().__init__(native)
        else:
            super().__init__(generated.ExternalInterface())


    def some_method(self, some_parameter: int):
        """"""
        return self._native.some_method(some_parameter)


    @property
    def some_property(self) -> str:
        """"""
        return self._native.some_property


from enum import Enum


class SomeEnum(Enum):
    """"""

    SOME_VALUE = 0

