

from dont.smoke.DontSmokeEnum import DontSmokeEnum

class SkippedFunctionClass:
    """"""

    def __init__(self, native):
        self._native = native


    def do_foo(self, input: DontSmokeEnum):
        """"""
        return self._native.do_foo(input)

