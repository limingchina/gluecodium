

from enum import Enum
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

    class LocaleStruct:
    
        locale_field: str
    
    
    
    LocaleTypeDef = str
    
    
    
    LocaleArray = list[str]
    
    
    
    LocaleMap = dict[str, str]
    
    
    
    LocaleSet = set[str]
    
    
    
    LocaleKeyMap = dict[str, str]
    
    

