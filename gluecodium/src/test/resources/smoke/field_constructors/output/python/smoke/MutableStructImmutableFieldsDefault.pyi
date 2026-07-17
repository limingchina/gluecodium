

from smoke.ImmutableDefaultCtor import ImmutableDefaultCtor


from _native_base import _NativeBase

import generated


class MutableStructImmutableFieldsDefault(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and hasattr(args[0], "_native"):
            super().__init__(args[0]._native)
        else:
            super().__init__(generated.MutableStructImmutableFieldsDefault(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def struct_field(self) -> ImmutableDefaultCtor:
        """"""
        return ImmutableDefaultCtor(self._native.struct_field)
    @struct_field.setter
    def struct_field(self, value: ImmutableDefaultCtor):
      self._native.struct_field = getattr(value, "_native", value)



    @property
    def int_field(self) -> int:
        """"""
        return self._native.int_field
    @int_field.setter
    def int_field(self, value: int):
      self._native.int_field = getattr(value, "_native", value)



    @property
    def bool_field(self) -> bool:
        """"""
        return self._native.bool_field
    @bool_field.setter
    def bool_field(self, value: bool):
      self._native.bool_field = getattr(value, "_native", value)


