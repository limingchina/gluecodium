

from __future__ import annotations



from _native_base import _NativeBase

import generated


class CachedProperties(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    @property
    def cached_property(self) -> list[str]:
        """"""
        return self._native.cached_property



    @property
    def internal_cached_property(self) -> list[str]:
        """"""
        return self._native.internal_cached_property



    @property
    def static_cached_property(self) -> bytes:
        """"""
        return self._native.static_cached_property



    @property
    def internal_static_cached_property(self) -> bytes:
        """"""
        return self._native.internal_static_cached_property


