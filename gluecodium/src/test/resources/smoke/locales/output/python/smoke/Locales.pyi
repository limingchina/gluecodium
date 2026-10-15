

from enum import Enum
import typing
from typing import Optional

class Locales:

    def locale_method(self, input: str) -> str:
        ...

    @property
    def locale_property(self) -> str:
        ...

    @locale_property.setter
    def locale_property(self, value: str) -> None:
        ...

    class LocaleStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, locale_field: str) -> None: ...

        locale_field: str



    LocaleTypeDef = str



    LocaleArray = list[str]



    LocaleMap = dict[str, str]



    LocaleSet = set[str]



    LocaleKeyMap = dict[str, str]
