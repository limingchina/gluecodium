

from __future__ import annotations



from _native_base import _NativeBase

import generated


class PublicFieldsMixedInit(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], PublicFieldsMixedInit):
            super().__init__(args[0])
        else:
            super().__init__(generated.PublicFieldsMixedInit(*args))


    @property
    def public_field1(self) -> str:
        """"""
        return self._native.public_field1

    @public_field1.setter
    def public_field1(self, value: str):
        self._native.public_field1 = value



    @property
    def public_field2(self) -> str:
        """"""
        return self._native.public_field2

    @public_field2.setter
    def public_field2(self, value: str):
        self._native.public_field2 = value



    @property
    def internal_field(self) -> str:
        """"""
        return self._native.internal_field

    @internal_field.setter
    def internal_field(self, value: str):
        self._native.internal_field = value


