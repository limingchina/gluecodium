

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional



from _native_base import _NativeBase

import generated


class LevelOneLevelTwoLevelThreeLevelFour(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_LevelOneLevelTwoLevelThreeLevelFour):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_LevelOneLevelTwoLevelThreeLevelFour(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def string_field(self) -> str:
        return _wrap(self._native.string_field, str)
    @string_field.setter
    def string_field(self, value: str):
      self._native.string_field = _unwrap(value, str)


    @staticmethod
    def foo_factory() -> LevelOneLevelTwoLevelThreeLevelFour:
        native_result = generated.smoke_LevelOneLevelTwoLevelThreeLevelFour.foo_factory()
        return _get_or_create_wrapper(native_result, LevelOneLevelTwoLevelThreeLevelFour)

    FOO = False

