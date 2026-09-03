

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class CachedProperties(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @property
    def cached_property(self) -> list[str]:
        return _wrap(self._native.cached_property, list[str])


    @property
    def _internal_cached_property(self) -> list[str]:
        return _wrap(self._native._internal_cached_property, list[str])


    @staticmethod
    def static_cached_property() -> bytes:
        return _wrap(generated.smoke_CachedProperties.static_cached_property(), bytes)

    @staticmethod
    def _internal_static_cached_property() -> bytes:
        return _wrap(generated.smoke_CachedProperties._internal_static_cached_property(), bytes)


