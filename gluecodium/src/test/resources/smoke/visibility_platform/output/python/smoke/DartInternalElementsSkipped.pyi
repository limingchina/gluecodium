



from _native_base import _NativeBase

import generated


class DartInternalElementsSkipped(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.DartInternalElementsSkipped):
            super().__init__(args[0])
        else:
            super().__init__(generated.DartInternalElementsSkipped(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def bool_field(self) -> bool:
        """"""
        return self._native.bool_field
    @bool_field.setter
    def bool_field(self, value: bool):
      self._native.bool_field = getattr(value, "_native", value)



    @property
    def string_field(self) -> str:
        """"""
        return self._native.string_field
    @string_field.setter
    def string_field(self, value: str):
      self._native.string_field = getattr(value, "_native", value)


    def foo(self):
        """"""
        return self._native.foo()

