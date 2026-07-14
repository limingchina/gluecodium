



from _native_base import _NativeBase

import generated


class DeprecatedFields(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], DeprecatedFields):
            super().__init__(args[0])
        else:
            super().__init__(generated.DeprecatedFields(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def normal_field1(self) -> str:
        """"""
        return self._native.normal_field1

    @normal_field1.setter
    def normal_field1(self, value: str):
      self._native.normal_field1 = getattr(value, "_native", value)



    @property
    def deprecated_field(self) -> str:
        """"""
        return self._native.deprecated_field

    @deprecated_field.setter
    def deprecated_field(self, value: str):
      self._native.deprecated_field = getattr(value, "_native", value)



    @property
    def normal_field2(self) -> str:
        """"""
        return self._native.normal_field2

    @normal_field2.setter
    def normal_field2(self, value: str):
      self._native.normal_field2 = getattr(value, "_native", value)


