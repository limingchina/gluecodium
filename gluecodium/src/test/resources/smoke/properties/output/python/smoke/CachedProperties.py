

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
    def __internal_cached_property(self) -> list[str]:
        return _wrap(self._native.__internal_cached_property, list[str])


    @staticmethod
    def static_cached_property() -> bytes:
        return _wrap(generated.smoke_CachedProperties.static_cached_property(), bytes)

    @staticmethod
    def __internal_static_cached_property() -> bytes:
        return _wrap(generated.smoke_CachedProperties.__internal_static_cached_property(), bytes)


