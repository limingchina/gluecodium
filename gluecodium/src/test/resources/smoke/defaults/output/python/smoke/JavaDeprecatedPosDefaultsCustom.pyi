

from smoke.JavaDeprecatedPosDefaultsCustom import JavaDeprecatedPosDefaultsCustom

from _native_base import _NativeBase


class JavaDeprecatedPosDefaultsCustom(_NativeBase):
    """Foo Bar this is a comment"""

    def __init__(self, native):
        super().__init__(native)

    first init!
    first_init_field: int

    first free!
    first_free_field: str


    def custom(self) -> JavaDeprecatedPosDefaultsCustom:
        """"""
        return self._native.custom()

