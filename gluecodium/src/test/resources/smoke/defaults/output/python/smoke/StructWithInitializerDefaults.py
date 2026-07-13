

from smoke.dict[int, str] import dict[int, str]
from smoke.list[float] import list[float]
from smoke.set[str] import set[str]

class StructWithInitializerDefaults:
    """"""

    def __init__(self, native):
        self._native = native


    ints_field: list[int]


    floats_field: list[float]


    set_type_field: set[str]


    map_field: dict[int, str]

