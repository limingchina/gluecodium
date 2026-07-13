

from smoke.SimpleClass import SimpleClass

from _native_base import _NativeBase


class SimpleClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def get_string_value(self) -> str:
        """"""
        return self._native.get_string_value()


    def use_simple_class(self, input: SimpleClass) -> SimpleClass:
        """"""
        return self._native.use_simple_class(input)

