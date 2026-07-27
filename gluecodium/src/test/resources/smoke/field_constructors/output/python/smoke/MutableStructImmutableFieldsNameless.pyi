

from smoke.ImmutableNamelessCtor import ImmutableNamelessCtor
import typing


from _native_base import _NativeBase

import generated


class MutableStructImmutableFieldsNameless(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_MutableStructImmutableFieldsNameless):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_MutableStructImmutableFieldsNameless(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def struct_field(self) -> ImmutableNamelessCtor:
        """"""
        return _wrap(self._native.struct_field, ImmutableNamelessCtor)
    @struct_field.setter
    def struct_field(self, value: ImmutableNamelessCtor):
      self._native.struct_field = _unwrap(value, ImmutableNamelessCtor)



    @property
    def int_field(self) -> int:
        """"""
        return _wrap(self._native.int_field, int)
    @int_field.setter
    def int_field(self, value: int):
      self._native.int_field = _unwrap(value, int)



    @property
    def bool_field(self) -> bool:
        """"""
        return _wrap(self._native.bool_field, bool)
    @bool_field.setter
    def bool_field(self, value: bool):
      self._native.bool_field = _unwrap(value, bool)


