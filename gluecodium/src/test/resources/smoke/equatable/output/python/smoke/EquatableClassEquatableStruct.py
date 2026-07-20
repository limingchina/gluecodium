

from __future__ import annotations

from smoke.PointerEquatableClass import PointerEquatableClass


from _native_base import _NativeBase

import generated


class EquatableClassEquatableStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.EquatableClassEquatableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.EquatableClassEquatableStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def int_field(self) -> int:
        """"""
        return self._native.int_field
    @int_field.setter
    def int_field(self, value: int):
      self._native.int_field = getattr(value, "_native", value)



    @property
    def string_field(self) -> str:
        """"""
        return self._native.string_field
    @string_field.setter
    def string_field(self, value: str):
      self._native.string_field = getattr(value, "_native", value)



    @property
    def nested_equatable_instance(self) -> EquatableClass:
        """"""
        from smoke.EquatableClass import EquatableClass
        return EquatableClass(self._native.nested_equatable_instance)
    @nested_equatable_instance.setter
    def nested_equatable_instance(self, value: EquatableClass):
      self._native.nested_equatable_instance = getattr(value, "_native", value)



    @property
    def nested_pointer_equatable_instance(self) -> PointerEquatableClass:
        """"""
        return PointerEquatableClass(self._native.nested_pointer_equatable_instance)
    @nested_pointer_equatable_instance.setter
    def nested_pointer_equatable_instance(self, value: PointerEquatableClass):
      self._native.nested_pointer_equatable_instance = getattr(value, "_native", value)


