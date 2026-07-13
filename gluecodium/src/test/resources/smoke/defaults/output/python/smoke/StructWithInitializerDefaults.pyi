

from smoke.dict[int, str] import dict[int, str]
from smoke.list[float] import list[float]
from smoke.set[str] import set[str]

from _native_base import _NativeBase


class StructWithInitializerDefaults(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    ints_field: list[int]


    floats_field: list[float]


    set_type_field: set[str]


    map_field: dict[int, str]

