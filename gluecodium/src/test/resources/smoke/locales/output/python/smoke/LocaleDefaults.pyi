

import typing


from _native_base import _NativeBase

import generated


class LocaleDefaults(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_LocaleDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_LocaleDefaults(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def english(self) -> str:
        """"""
        return _wrap(self._native.english, str)
    @english.setter
    def english(self, value: str):
      self._native.english = _unwrap(value, str)



    @property
    def lat_am_spanish(self) -> str:
        """"""
        return _wrap(self._native.lat_am_spanish, str)
    @lat_am_spanish.setter
    def lat_am_spanish(self, value: str):
      self._native.lat_am_spanish = _unwrap(value, str)



    @property
    def romansh_sursilvan(self) -> str:
        """"""
        return _wrap(self._native.romansh_sursilvan, str)
    @romansh_sursilvan.setter
    def romansh_sursilvan(self, value: str):
      self._native.romansh_sursilvan = _unwrap(value, str)



    @property
    def serbian_cyrillic(self) -> str:
        """"""
        return _wrap(self._native.serbian_cyrillic, str)
    @serbian_cyrillic.setter
    def serbian_cyrillic(self, value: str):
      self._native.serbian_cyrillic = _unwrap(value, str)



    @property
    def traditional_chinese_taiwan(self) -> str:
        """"""
        return _wrap(self._native.traditional_chinese_taiwan, str)
    @traditional_chinese_taiwan.setter
    def traditional_chinese_taiwan(self, value: str):
      self._native.traditional_chinese_taiwan = _unwrap(value, str)



    @property
    def zuerich_german(self) -> str:
        """"""
        return _wrap(self._native.zuerich_german, str)
    @zuerich_german.setter
    def zuerich_german(self, value: str):
      self._native.zuerich_german = _unwrap(value, str)


