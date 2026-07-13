

from smoke.PublicStructWithInternalConstructors import PublicStructWithInternalConstructors

class PublicStructWithInternalConstructors:
    """"""

    def __init__(self, native):
        self._native = native


    some_var: int


    def make(self) -> PublicStructWithInternalConstructors:
        """"""
        return self._native.make()

