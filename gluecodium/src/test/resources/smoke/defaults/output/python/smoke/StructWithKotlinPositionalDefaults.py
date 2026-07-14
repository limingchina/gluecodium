

from __future__ import annotations



from _native_base import _NativeBase

import generated


class StructWithKotlinPositionalDefaults(_NativeBase):
    """This is an important struct that uses positional default annotation."""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], StructWithKotlinPositionalDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructWithKotlinPositionalDefaults(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def first_init_field(self) -> int:
        """"""
        return self._native.first_init_field

    @first_init_field.setter
    def first_init_field(self, value: int):
      self._native.first_init_field = getattr(value, "_native", value)



    @property
    def first_free_field(self) -> str:
        """"""
        return self._native.first_free_field

    @first_free_field.setter
    def first_free_field(self, value: str):
      self._native.first_free_field = getattr(value, "_native", value)



    @property
    def second_init_field(self) -> float:
        """"""
        return self._native.second_init_field

    @second_init_field.setter
    def second_init_field(self, value: float):
      self._native.second_init_field = getattr(value, "_native", value)



    @property
    def second_free_field(self) -> bool:
        """"""
        return self._native.second_free_field

    @second_free_field.setter
    def second_free_field(self, value: bool):
      self._native.second_free_field = getattr(value, "_native", value)



    @property
    def third_init_field(self) -> str:
        """"""
        return self._native.third_init_field

    @third_init_field.setter
    def third_init_field(self, value: str):
      self._native.third_init_field = getattr(value, "_native", value)


