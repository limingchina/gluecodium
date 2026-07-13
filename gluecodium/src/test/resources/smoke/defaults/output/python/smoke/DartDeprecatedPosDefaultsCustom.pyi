

from smoke.DartDeprecatedPosDefaultsCustom import DartDeprecatedPosDefaultsCustom

from _native_base import _NativeBase


class DartDeprecatedPosDefaultsCustom(_NativeBase):
    """Foo Bar this is a comment"""

    def __init__(self, native):
        super().__init__(native)


    int_field: int


    string_field: str


    def custom(self) -> DartDeprecatedPosDefaultsCustom:
        """"""
        return self._native.custom()

