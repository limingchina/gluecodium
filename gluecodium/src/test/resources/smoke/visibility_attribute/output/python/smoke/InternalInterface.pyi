



from _native_base import _NativeBase

import generated


class InternalInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, InternalInterface):
            super().__init__(native)
        else:
            super().__init__(generated.InternalInterface())


    def foo_bar(self):
        """"""
        return self._native.foo_bar()


    @property
    def some_property_of_internal_interface(self) -> str:
        """"""
        return self._native.some_property_of_internal_interface

    @some_property_of_internal_interface.setter
    def some_property_of_internal_interface(self, value: str):
        self._native.some_property_of_internal_interface = value

