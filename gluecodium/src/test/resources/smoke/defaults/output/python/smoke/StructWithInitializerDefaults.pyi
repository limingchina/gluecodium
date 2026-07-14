



from _native_base import _NativeBase

import generated


class StructWithInitializerDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], StructWithInitializerDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructWithInitializerDefaults(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def ints_field(self) -> list[int]:
        """"""
        return self._native.ints_field

    @ints_field.setter
    def ints_field(self, value: list[int]):
      self._native.ints_field = getattr(value, "_native", value)



    @property
    def floats_field(self) -> list[float]:
        """"""
        return self._native.floats_field

    @floats_field.setter
    def floats_field(self, value: list[float]):
      self._native.floats_field = getattr(value, "_native", value)



    @property
    def set_type_field(self) -> set[str]:
        """"""
        return self._native.set_type_field

    @set_type_field.setter
    def set_type_field(self, value: set[str]):
      self._native.set_type_field = getattr(value, "_native", value)



    @property
    def map_field(self) -> dict[int, str]:
        """"""
        return self._native.map_field

    @map_field.setter
    def map_field(self, value: dict[int, str]):
      self._native.map_field = getattr(value, "_native", value)


