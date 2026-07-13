

from smoke.JavaDeprecatedPosDefaultsCustom import JavaDeprecatedPosDefaultsCustom

class JavaDeprecatedPosDefaultsCustom:
    """Foo Bar this is a comment"""

    def __init__(self, native):
        self._native = native

    first init!
    first_init_field: int

    first free!
    first_free_field: str


    def custom(self) -> JavaDeprecatedPosDefaultsCustom:
        """"""
        return self._native.custom()

