

from smoke.Annotations import Annotations

class Annotations:
    """"""

    def __init__(self, native):
        self._native = native


    def test_optional(self, self: Annotations) -> Optional[bool]:
        """"""
        return self._native.test_optional(self)

