



from _native_base import _NativeBase

import generated


class SimpleInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, SimpleInterface):
            super().__init__(native)
        else:
            super().__init__(generated.SimpleInterface())


    def get_string_value(self) -> str:
        """"""
        return self._native.get_string_value()


    def use_simple_interface(self, input: SimpleInterface) -> SimpleInterface:
        """"""
        return self._native.use_simple_interface(input._native)

