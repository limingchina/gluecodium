

from smoke.dict[str, int] import dict[str, int]
from smoke.list[str] import list[str]

class DartInternalClassWithInternalTypedef:
    """"""

    def __init__(self, native):
        self._native = native


    @property
    def numbers(self) -> dict[str, int]:
        """"""
        return self._native.numbers



    @property
    def labels(self) -> list[str]:
        """"""
        return self._native.labels


