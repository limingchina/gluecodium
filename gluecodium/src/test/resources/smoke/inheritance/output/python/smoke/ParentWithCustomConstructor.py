

from smoke.ParentWithCustomConstructor import ParentWithCustomConstructor

class ParentWithCustomConstructor:
    """"""

    def __init__(self, native):
        self._native = native


    def create(self) -> ParentWithCustomConstructor:
        """"""
        return self._native.create()

