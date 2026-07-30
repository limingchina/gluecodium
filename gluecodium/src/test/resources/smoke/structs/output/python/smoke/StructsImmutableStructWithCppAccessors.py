

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.StructsPoint import StructsPoint


from _native_base import _NativeBase

import generated


class StructsImmutableStructWithCppAccessors(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_StructsImmutableStructWithCppAccessors):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_StructsImmutableStructWithCppAccessors(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def trivial_int_field(self) -> int:
        return _wrap(self._native.trivial_int_field, int)


    @property
    def trivial_double_field(self) -> float:
        return _wrap(self._native.trivial_double_field, float)


    @property
    def nontrivial_string_field(self) -> str:
        return _wrap(self._native.nontrivial_string_field, str)


    @property
    def nontrivial_point_field(self) -> StructsPoint:
        return _wrap(self._native.nontrivial_point_field, StructsPoint)


    @property
    def nontrivial_optional_point(self):
        return _wrap(self._native.nontrivial_optional_point, Optional[StructsPoint])


