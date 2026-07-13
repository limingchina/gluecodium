

from smoke.InnerStructWithDefaults import InnerStructWithDefaults


from _native_base import _NativeBase

import generated


class OuterStructWithFieldConstructor(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], OuterStructWithFieldConstructor):
            super().__init__(args[0])
        else:
            super().__init__(generated.OuterStructWithFieldConstructor(*args))


    @property
    def outer_struct_field(self) -> InnerStructWithDefaults:
        """"""
        return self._native.outer_struct_field

    @outer_struct_field.setter
    def outer_struct_field(self, value: InnerStructWithDefaults):
        self._native.outer_struct_field = value


