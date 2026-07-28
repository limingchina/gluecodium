

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

import datetime
from smoke.FreeEnum import FreeEnum
from smoke.FreeError import FreeError
from smoke.FreePoint import FreePoint

from _native_base import _NativeBase

import generated


class UseFreeTypes(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def do_stuff(self, point: FreePoint, mode: FreeEnum) -> datetime.datetime:
        """"""
        return _wrap(self._native.do_stuff(_unwrap(point, FreePoint), _unwrap(mode, FreeEnum)), datetime.datetime)

