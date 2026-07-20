

from smoke.DefaultValuesStructWithDefaults import DefaultValuesStructWithDefaults
import typing

from _native_base import _NativeBase

import generated


class DefaultValues(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def process_struct_with_defaults(input: DefaultValuesStructWithDefaults) -> DefaultValuesStructWithDefaults: ...

