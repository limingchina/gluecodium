

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

import datetime
from smoke.NullableSomeStruct import NullableSomeStruct


from _native_base import _NativeBase

import generated


class NullableCollectionsStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_NullableCollectionsStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_NullableCollectionsStruct(*[_unwrap(arg) for arg in args]))


    @property
    def dates(self) -> list[Optional[datetime.datetime]]:
        """"""
        return _wrap(self._native.dates, list[Optional[datetime.datetime]])
    @dates.setter
    def dates(self, value: list[Optional[datetime.datetime]]):
      self._native.dates = _unwrap(value, list[Optional[datetime.datetime]])



    @property
    def structs(self) -> dict[int, Optional[NullableSomeStruct]]:
        """"""
        return _wrap(self._native.structs, dict[int, Optional[NullableSomeStruct]])
    @structs.setter
    def structs(self, value: dict[int, Optional[NullableSomeStruct]]):
      self._native.structs = _unwrap(value, dict[int, Optional[NullableSomeStruct]])


