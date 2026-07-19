



from _native_base import _NativeBase

import generated


class EnumCollectionDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.EnumCollectionDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.EnumCollectionDefaults(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def list_field(self) -> list[Enum1]:
        """"""
        return self._native.list_field
    @list_field.setter
    def list_field(self, value: list[Enum1]):
      self._native.list_field = getattr(value, "_native", value)



    @property
    def set_field(self) -> set[Enum2]:
        """"""
        return self._native.set_field
    @set_field.setter
    def set_field(self, value: set[Enum2]):
      self._native.set_field = getattr(value, "_native", value)



    @property
    def map_field(self) -> dict[Enum3, Enum4]:
        """"""
        return self._native.map_field
    @map_field.setter
    def map_field(self, value: dict[Enum3, Enum4]):
      self._native.map_field = getattr(value, "_native", value)


