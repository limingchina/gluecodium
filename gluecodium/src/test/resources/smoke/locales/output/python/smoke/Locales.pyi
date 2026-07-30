

import typing

class Locales:

    def locale_method(self, input: str) -> str:
        ...

    @property
    def locale_property(self) -> str:
        ...

    @locale_property.setter
    def locale_property(self, value: str) -> None:
        ...

