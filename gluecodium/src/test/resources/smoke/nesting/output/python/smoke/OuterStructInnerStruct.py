

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

import datetime


from _native_base import _NativeBase

import generated


class OuterStructInnerStruct(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_OuterStructInnerStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_OuterStructInnerStruct(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def other_field(self) -> list[datetime.datetime]:
        return _wrap(self._native.other_field, list[datetime.datetime])
    @other_field.setter
    def other_field(self, value: list[datetime.datetime]):
      self._native.other_field = _unwrap(value, list[datetime.datetime])


    def do_something(self):
        return _wrap(self._native.do_something(), None)

