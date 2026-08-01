

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
from typing import Callable
import generated


class Lambdas(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def deconfuse(self, value: str, confuser: Callable[[str], Callable[[], str]]) -> Callable[[], str]:
        return _wrap(self._native.deconfuse(_unwrap(value, str), _unwrap(confuser, Callable[[str], Callable[[], str]])), Callable[[], str])

    @staticmethod
    def fuse(items: list[str], callback: Callable[[str, float], int]) -> dict[int, str]:
        return _wrap(generated.smoke_Lambdas.fuse(_unwrap(items, list[str]), _unwrap(callback, Callable[[str, float], int])), dict[int, str])

    Producer = Callable[[], str]
    
    
    
    #: Should confuse everyone thoroughly
    Confuser = Callable[[str], Callable[[], str]]
    
    
    
    Consumer = Callable[[str], None]
    
    
    
    Indexer = Callable[[str, float], int]
    
    
    
    NullableConfuser = Callable[[Optional[str]], Optional[Callable[[], str]]]
    
    

