

from smoke.SimpleInterface import SimpleInterface

from _native_base import _NativeBase


class SimpleInterface(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def get_string_value(self) -> str:
        """"""
        return self._native.get_string_value()


    def use_simple_interface(self, input: SimpleInterface) -> SimpleInterface:
        """"""
        return self._native.use_simple_interface(input)

