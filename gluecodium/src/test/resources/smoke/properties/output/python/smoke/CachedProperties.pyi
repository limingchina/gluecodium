

import typing

class CachedProperties:

    @property
    def cached_property(self) -> list[str]:
        ...


    @property
    def static_cached_property(self) -> bytes:
        ...


