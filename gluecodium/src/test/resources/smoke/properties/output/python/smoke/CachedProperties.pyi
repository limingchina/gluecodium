

from enum import Enum
import typing

class CachedProperties:

    @property
    def cached_property(self) -> list[str]:
        ...


    @property
    def _internal_cached_property(self) -> list[str]:
        ...


    @property
    def static_cached_property(self) -> bytes:
        ...


    @property
    def _internal_static_cached_property(self) -> bytes:
        ...



