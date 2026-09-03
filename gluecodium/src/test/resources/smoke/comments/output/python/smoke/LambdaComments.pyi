

from enum import Enum
import typing
from typing import Callable

class LambdaComments:

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
    
    

