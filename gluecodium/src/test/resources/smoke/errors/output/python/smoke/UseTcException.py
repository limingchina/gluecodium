

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.SomeTypeCollectionSome import SomeTypeCollectionSome
from smoke.SomeTypeCollectionSomeTypeCollectionError import SomeTypeCollectionSomeTypeCollectionError

from _native_base import _NativeBase

import generated


class UseTcException(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def do_nothing(self):
        """"""
        return _wrap(self._native.do_nothing(), None)

