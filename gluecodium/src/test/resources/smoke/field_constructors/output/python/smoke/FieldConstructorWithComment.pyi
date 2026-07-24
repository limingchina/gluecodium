

import typing


from _native_base import _NativeBase

import generated


class FieldConstructorWithComment(_NativeBase):
    """SomeStruct"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.FieldConstructorWithComment):
            super().__init__(args[0])
        else:
            super().__init__(generated.FieldConstructorWithComment(*[_unwrap(arg) for arg in args]))

    Some field
    @property
    def string_field(self) -> str:
        """Some field"""
        return _wrap(self._native.string_field, str)
    @string_field.setter
    def string_field(self, value: str):
      self._native.string_field = _unwrap(value, str)


