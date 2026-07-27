

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class EquatableStructWithInternalFields(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_EquatableStructWithInternalFields):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_EquatableStructWithInternalFields(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self._native == other._native

    def __hash__(self) -> int:
        return hash(self._native)


    @property
    def public_field(self) -> str:
        """"""
        return _wrap(self._native.public_field, str)
    @public_field.setter
    def public_field(self, value: str):
      self._native.public_field = _unwrap(value, str)



    @property
    def internal_field(self) -> str:
        """"""
        return _wrap(self._native.internal_field, str)
    @internal_field.setter
    def internal_field(self, value: str):
      self._native.internal_field = _unwrap(value, str)



    @property
    def internal_list_field(self) -> list[str]:
        """"""
        return _wrap(self._native.internal_list_field, list[str])
    @internal_list_field.setter
    def internal_list_field(self, value: list[str]):
      self._native.internal_list_field = _unwrap(value, list[str])



    @property
    def internal_map_field(self) -> dict[str, str]:
        """"""
        return _wrap(self._native.internal_map_field, dict[str, str])
    @internal_map_field.setter
    def internal_map_field(self, value: dict[str, str]):
      self._native.internal_map_field = _unwrap(value, dict[str, str])



    @property
    def internal_set_field(self) -> set[str]:
        """"""
        return _wrap(self._native.internal_set_field, set[str])
    @internal_set_field.setter
    def internal_set_field(self, value: set[str]):
      self._native.internal_set_field = _unwrap(value, set[str])


