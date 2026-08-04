

from enum import Enum
import typing

class CachedProperties:

    @property
    def cached_property(self) -> list[str]:
        ...


    @property
    def __internal_cached_property(self) -> list[str]:
        ...


    @property
    def static_cached_property(self) -> bytes:
        ...


    @property
    def __internal_static_cached_property(self) -> bytes:
        ...



