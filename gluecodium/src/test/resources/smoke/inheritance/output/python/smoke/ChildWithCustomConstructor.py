

from smoke.ChildWithCustomConstructor import ChildWithCustomConstructor
from smoke.ParentWithCustomConstructor import ParentWithCustomConstructor

class ChildWithCustomConstructor(
    ParentWithCustomConstructor):
    """"""

    def __init__(self, native):
        self._native = native


    def make(self) -> ChildWithCustomConstructor:
        """"""
        return self._native.make()

