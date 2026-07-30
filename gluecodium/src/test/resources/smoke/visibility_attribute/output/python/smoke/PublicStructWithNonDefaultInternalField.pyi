

import typing


from _native_base import _NativeBase

import generated


class PublicStructWithNonDefaultInternalField(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_PublicStructWithNonDefaultInternalField):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_PublicStructWithNonDefaultInternalField(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def defaulted_field(self) -> int:
        """"""
        return _wrap(self._native.defaulted_field, int)
    @defaulted_field.setter
    def defaulted_field(self, value: int):
      self._native.defaulted_field = _unwrap(value, int)



    @property
    def public_field(self) -> bool:
        """"""
        return _wrap(self._native.public_field, bool)
    @public_field.setter
    def public_field(self, value: bool):
      self._native.public_field = _unwrap(value, bool)


