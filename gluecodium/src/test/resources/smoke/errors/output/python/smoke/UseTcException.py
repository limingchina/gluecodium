

from smoke.SomeError import SomeError
from smoke.SomeTypeCollectionError import SomeTypeCollectionError

class UseTcException:
    """"""

    def __init__(self, native):
        self._native = native


    def do_nothing(self):
        """"""
        return self._native.do_nothing()

