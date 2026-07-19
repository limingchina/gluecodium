



from _native_base import _NativeBase

import generated


class OuterInternalStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.OuterInternalStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.OuterInternalStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def some_field(self) -> int:
        """"""
        return self._native.some_field
    @some_field.setter
    def some_field(self, value: int):
      self._native.some_field = getattr(value, "_native", value)


