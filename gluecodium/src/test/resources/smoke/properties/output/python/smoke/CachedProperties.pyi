



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



    @staticmethod
    def static_cached_property() -> bytes:
        """"""
        return generated.CachedProperties.static_cached_property()


    @staticmethod
    def internal_static_cached_property() -> bytes:
        """"""
        return generated.CachedProperties.internal_static_cached_property()

