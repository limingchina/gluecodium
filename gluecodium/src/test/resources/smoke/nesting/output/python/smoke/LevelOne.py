

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.OuterClass import OuterClass
from smoke.OuterInterface import OuterInterface

class LevelOne(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    class LevelTwo(_NativeBase):
        def __init__(self, native):
            super().__init__(native)
    
        class LevelThree(_NativeBase):
            def __init__(self, native):
                super().__init__(native)
    
            def foo(self, input: OuterClass.InnerInterface) -> OuterInterface.InnerClass:
                return _wrap(self._native.foo(_unwrap(input, OuterClass.InnerInterface)), OuterInterface.InnerClass)
    
            class LevelFour(_NativeBase):
                def __init__(self, *args, **kwargs):
                    if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_LevelOne.LevelTwo.LevelThree.LevelFour):
                        super().__init__(args[0])
                    else:
                        super().__init__(generated.smoke_LevelOne.LevelTwo.LevelThree.LevelFour(
                            *[_unwrap(arg) for arg in args],
                            **{k: _unwrap(v) for k, v in kwargs.items()}
                        ))
    
                @property
                def string_field(self) -> str:
                    return _wrap(self._native.string_field, str)
                @string_field.setter
                def string_field(self, value: str):
                  self._native.string_field = _unwrap(value, str)
    
    
                @staticmethod
                def foo_factory() -> LevelOne.LevelTwo.LevelThree.LevelFour:
                    native_result = generated.smoke_LevelOne.LevelTwo.LevelThree.LevelFour.foo_factory()
                    return _get_or_create_wrapper(native_result, LevelOne.LevelTwo.LevelThree.LevelFour)
    
    
                FOO = False
    
    
            class LevelFourEnum(Enum):
    
                NONE = generated.smoke_LevelOne.LevelTwo.LevelThree.LevelFourEnum.NONE
    
                @property
                def _native(self):
                    return self.value
    
    
    
    

