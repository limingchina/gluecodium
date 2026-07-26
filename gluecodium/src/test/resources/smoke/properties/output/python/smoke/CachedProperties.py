

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from _native_base import _NativeBase

import generated


class CachedProperties(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @property
    def cached_property(self) -> list[str]:
        """"""
        return _wrap(self._native.cached_property, list[str])


    @property
    def internal_cached_property(self) -> list[str]:
        """"""
        return _wrap(self._native.internal_cached_property, list[str])



    @staticmethod
    def static_cached_property() -> bytes:
        """"""
        return _wrap(generated.smoke_CachedProperties.static_cached_property(), bytes)


    @staticmethod
    def internal_static_cached_property() -> bytes:
        """"""
        return _wrap(generated.smoke_CachedProperties.internal_static_cached_property(), bytes)

