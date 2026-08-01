

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
    
    
    
    str = str
    
    
    
    list[str] = list[str]
    
    
    
    dict[str, str] = dict[str, str]
    
    
    
    set[str] = set[str]
    
    
    
    dict[str, str] = dict[str, str]
    
    

