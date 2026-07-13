


class OverloadsWithComments:
    """"""

    def __init__(self, native):
        self._native = native


    def do_stuff(self):
        """"""
        return self._native.do_stuff()

    [stuff]
    def do_stuff(self, stuff: str):
        """[stuff]"""
        return self._native.do_stuff(stuff)

