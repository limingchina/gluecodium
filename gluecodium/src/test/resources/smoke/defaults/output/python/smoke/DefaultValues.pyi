

from smoke.StructWithDefaults import StructWithDefaults
from smoke.bool import bool
from smoke.dict[int, str] import dict[int, str]
from smoke.int import int
from smoke.list[float] import list[float]
from smoke.set[str] import set[str]
from smoke.str import str


from _native_base import _NativeBase

import generated


class DefaultValues(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod

    def process_struct_with_defaults(input: StructWithDefaults) -> StructWithDefaults:
        """"""
        native_result = generated.DefaultValues.process_struct_with_defaults(input)
        return StructWithDefaults(native_result)

