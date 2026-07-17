

from smoke.OuterStructWithFieldConstructorInnerStructWithDefaults import OuterStructWithFieldConstructorInnerStructWithDefaults


from _native_base import _NativeBase

import generated


class OuterStructWithFieldConstructor(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.OuterStructWithFieldConstructor):
            super().__init__(args[0])
        else:
            super().__init__(generated.OuterStructWithFieldConstructor(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def outer_struct_field(self) -> OuterStructWithFieldConstructorInnerStructWithDefaults:
        """"""
        return OuterStructWithFieldConstructorInnerStructWithDefaults(self._native.outer_struct_field)
    @outer_struct_field.setter
    def outer_struct_field(self, value: OuterStructWithFieldConstructorInnerStructWithDefaults):
      self._native.outer_struct_field = getattr(value, "_native", value)


