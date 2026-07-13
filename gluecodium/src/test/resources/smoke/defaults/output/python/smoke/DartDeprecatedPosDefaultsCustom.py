

from smoke.DartDeprecatedPosDefaultsCustom import DartDeprecatedPosDefaultsCustom

class DartDeprecatedPosDefaultsCustom:
    """Foo Bar this is a comment"""

    def __init__(self, native):
        self._native = native


    int_field: int


    string_field: str


    def custom(self) -> DartDeprecatedPosDefaultsCustom:
        """"""
        return self._native.custom()

