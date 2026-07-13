

from smoke.Annotations import Annotations

from _native_base import _NativeBase


class Annotations(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def test_optional(self, self: Annotations) -> Optional[bool]:
        """"""
        return self._native.test_optional(self)

