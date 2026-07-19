



from _native_base import _NativeBase

import generated


class AsyncStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.AsyncStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.AsyncStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def string_field(self) -> str:
        """"""
        return self._native.string_field
    @string_field.setter
    def string_field(self, value: str):
      self._native.string_field = getattr(value, "_native", value)


    def async_void(self, input: bool):
        """"""
        return self._native.async_void(input)

    def async_void_throws(self, input: bool):
        """"""
        return self._native.async_void_throws(input)

    def async_int(self, input: bool) -> int:
        """"""
        return self._native.async_int(input)

    def async_int_throws(self, input: bool) -> int:
        """"""
        return self._native.async_int_throws(input)

    @staticmethod
    def async_static(input: bool):
        """"""
        generated.AsyncStruct.async_static(input)

