


class SkipTypes:
    """"""

    def __init__(self, native):
        self._native = native


    def use_list_in_dart(self) -> list[NotInDart]:
        """"""
        return self._native.use_list_in_dart()

