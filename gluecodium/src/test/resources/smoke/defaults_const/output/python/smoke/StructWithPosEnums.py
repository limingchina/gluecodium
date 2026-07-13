

from smoke.FIRST_CONSTANT import FIRST_CONSTANT
from smoke.SomethingEnum import SomethingEnum

class StructWithPosEnums:
    """"""

    def __init__(self, native):
        self._native = native


    first_field: SomethingEnum


    explicit_field: SomethingEnum


    last_field: SomethingEnum

