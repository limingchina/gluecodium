

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.DefaultValuesStructWithDefaults import DefaultValuesStructWithDefaults

from _native_base import _NativeBase

import generated


class DefaultValues(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def process_struct_with_defaults(input: DefaultValuesStructWithDefaults) -> DefaultValuesStructWithDefaults:
        native_result = generated.smoke_DefaultValues.process_struct_with_defaults(_unwrap(input, DefaultValuesStructWithDefaults))
        return _get_or_create_wrapper(native_result, DefaultValuesStructWithDefaults)

