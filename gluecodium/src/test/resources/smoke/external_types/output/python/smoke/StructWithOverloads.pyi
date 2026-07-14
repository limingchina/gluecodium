



from _native_base import _NativeBase

import generated


class StructWithOverloads(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], StructWithOverloads):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructWithOverloads(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def overloaded_accessors(self) -> int:
        """"""
        return self._native.overloaded_accessors

    @overloaded_accessors.setter
    def overloaded_accessors(self, value: int):
      self._native.overloaded_accessors = getattr(value, "_native", value)


    def overloaded_method(self) -> str:
        """"""
        return self._native.overloaded_method()

    def overloaded_method(self, input: str) -> str:
        """"""
        return self._native.overloaded_method(input)

    def overloaded_method(self, input_string: str, input_bool: bool) -> str:
        """"""
        return self._native.overloaded_method(input_string, input_bool)

