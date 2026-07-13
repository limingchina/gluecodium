

from dont.smoke.DontSmokeEnum import DontSmokeEnum

class SomeSkippedClass:
    """"""

    def __init__(self, native):
        self._native = native


    def do_foo(self) -> DontSmokeEnum:
        """"""
        return self._native.do_foo()

