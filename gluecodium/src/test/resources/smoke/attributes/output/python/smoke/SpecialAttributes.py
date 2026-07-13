


class SpecialAttributes:
    """"""

    def __init__(self, native):
        self._native = native


    def with_escaping(self):
        """"""
        return self._native.with_escaping()


    def with_line_break(self):
        """"""
        return self._native.with_line_break()

