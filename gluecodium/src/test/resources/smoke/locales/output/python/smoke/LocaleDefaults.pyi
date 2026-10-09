

from enum import Enum
import typing
from typing import Optional

class LocaleDefaults:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, english: str, lat_am_spanish: str, romansh_sursilvan: str, serbian_cyrillic: str, traditional_chinese_taiwan: str, zuerich_german: str) -> None: ...

    english: str

    lat_am_spanish: str

    romansh_sursilvan: str

    serbian_cyrillic: str

    traditional_chinese_taiwan: str

    zuerich_german: str
