

from __future__ import annotations

from smoke.DefaultValuesStructWithDefaults import DefaultValuesStructWithDefaults

from _native_base import _NativeBase

import generated


class DefaultValues(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def process_struct_with_defaults(input: DefaultValuesStructWithDefaults) -> DefaultValuesStructWithDefaults:
        """"""
        native_result = generated.DefaultValues.process_struct_with_defaults(input._native)
        return DefaultValuesStructWithDefaults(native_result)

