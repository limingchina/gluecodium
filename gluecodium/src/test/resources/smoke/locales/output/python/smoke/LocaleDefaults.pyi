



from _native_base import _NativeBase

import generated


class LocaleDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], LocaleDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.LocaleDefaults(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def english(self) -> str:
        """"""
        return self._native.english

    @english.setter
    def english(self, value: str):
      self._native.english = getattr(value, "_native", value)



    @property
    def lat_am_spanish(self) -> str:
        """"""
        return self._native.lat_am_spanish

    @lat_am_spanish.setter
    def lat_am_spanish(self, value: str):
      self._native.lat_am_spanish = getattr(value, "_native", value)



    @property
    def romansh_sursilvan(self) -> str:
        """"""
        return self._native.romansh_sursilvan

    @romansh_sursilvan.setter
    def romansh_sursilvan(self, value: str):
      self._native.romansh_sursilvan = getattr(value, "_native", value)



    @property
    def serbian_cyrillic(self) -> str:
        """"""
        return self._native.serbian_cyrillic

    @serbian_cyrillic.setter
    def serbian_cyrillic(self, value: str):
      self._native.serbian_cyrillic = getattr(value, "_native", value)



    @property
    def traditional_chinese_taiwan(self) -> str:
        """"""
        return self._native.traditional_chinese_taiwan

    @traditional_chinese_taiwan.setter
    def traditional_chinese_taiwan(self, value: str):
      self._native.traditional_chinese_taiwan = getattr(value, "_native", value)



    @property
    def zuerich_german(self) -> str:
        """"""
        return self._native.zuerich_german

    @zuerich_german.setter
    def zuerich_german(self, value: str):
      self._native.zuerich_german = getattr(value, "_native", value)


