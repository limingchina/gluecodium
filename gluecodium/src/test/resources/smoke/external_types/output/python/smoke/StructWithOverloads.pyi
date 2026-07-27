

import typing


from _native_base import _NativeBase

import generated


class StructWithOverloads(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_StructWithOverloads):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_StructWithOverloads(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def overloaded_accessors(self) -> int:
        """"""
        return _wrap(self._native.overloaded_accessors, int)
    @overloaded_accessors.setter
    def overloaded_accessors(self, value: int):
      self._native.overloaded_accessors = _unwrap(value, int)


    @typing.overload
    def overloaded_method(self) -> str: ...

    @typing.overload
    def overloaded_method(self, input: str) -> str: ...

    @typing.overload
    def overloaded_method(self, input_string: str, input_bool: bool) -> str: ...

