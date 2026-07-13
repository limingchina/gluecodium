

from smoke.TCEnum import TCEnum

class EnumsInTypeCollectionInterface:
    """"""

    def __init__(self, native):
        self._native = native


    def flip_enum_value(self, input: TCEnum) -> TCEnum:
        """"""
        return self._native.flip_enum_value(input)

