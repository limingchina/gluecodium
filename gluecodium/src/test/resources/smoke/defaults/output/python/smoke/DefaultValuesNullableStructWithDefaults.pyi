

import typing


from _native_base import _NativeBase

import generated


class DefaultValuesNullableStructWithDefaults(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DefaultValuesNullableStructWithDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_DefaultValuesNullableStructWithDefaults(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def int_field(self):
        """"""
        return _wrap(self._native.int_field, Optional[int])
    @int_field.setter
    def int_field(self, value):
      self._native.int_field = _unwrap(value, Optional[int])



    @property
    def uint_field(self):
        """"""
        return _wrap(self._native.uint_field, Optional[int])
    @uint_field.setter
    def uint_field(self, value):
      self._native.uint_field = _unwrap(value, Optional[int])



    @property
    def float_field(self):
        """"""
        return _wrap(self._native.float_field, Optional[float])
    @float_field.setter
    def float_field(self, value):
      self._native.float_field = _unwrap(value, Optional[float])



    @property
    def bool_field(self):
        """"""
        return _wrap(self._native.bool_field, Optional[bool])
    @bool_field.setter
    def bool_field(self, value):
      self._native.bool_field = _unwrap(value, Optional[bool])



    @property
    def string_field(self):
        """"""
        return _wrap(self._native.string_field, Optional[str])
    @string_field.setter
    def string_field(self, value):
      self._native.string_field = _unwrap(value, Optional[str])


