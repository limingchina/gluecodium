

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
from typing import Callable
import generated


class LambdaComments(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    #: The first line of the doc.
    WithNoNamedParameters = Callable[[str], str]
    
    
    
    #: The first line of the doc.
    WithNoDocsForParameters = Callable[[str], str]
    
    
    
    #: The first line of the doc.
    WithNamedParameters = Callable[[str], str]
    
    
    
    #: The first line of the doc.
    MixedDocNameParameters = Callable[[str, str], str]
    
    
    
    NoCommentsNoNamedParams = Callable[[str, str], str]
    
    
    
    NoCommentsWithNamedParams = Callable[[str, str], str]
    
    

