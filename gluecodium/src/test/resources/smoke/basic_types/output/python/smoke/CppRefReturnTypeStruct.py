

from __future__ import annotations



from _native_base import _NativeBase

import generated


class CppRefReturnTypeStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], CppRefReturnTypeStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.CppRefReturnTypeStruct(*args))

    @staticmethod

    def string_ref() -> str:
        """"""
        native_result = generated.CppRefReturnTypeStruct.string_ref()
        return str(native_result)

