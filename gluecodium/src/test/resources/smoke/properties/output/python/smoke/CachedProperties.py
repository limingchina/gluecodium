


class CachedProperties:
    """"""

    def __init__(self, native):
        self._native = native


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


