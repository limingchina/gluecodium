

from smoke.InnerName import InnerName

class UseInnerName:
    """"""

    def __init__(self, native):
        self._native = native


    def do_foo(self) -> InnerName:
        """"""
        return self._native.do_foo()

