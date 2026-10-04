

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base
from enum import Enum
from typing import Optional
import generated


@_mark_callback_base
class ListenerWithNullable(generated.smoke_ListenerWithNullable):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("method_with_byte", "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f645769746842797465", "method", None,
             lambda: ([Optional[int]], Optional[int])),
            ("method_with_u_byte", "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f64576974685542797465", "method", None,
             lambda: ([Optional[int]], Optional[int])),
            ("method_with_short", "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f645769746853686f7274", "method", None,
             lambda: ([Optional[int]], Optional[int])),
            ("method_with_u_short", "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f64576974685553686f7274", "method", None,
             lambda: ([Optional[int]], Optional[int])),
            ("method_with_int", "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f6457697468496e74", "method", None,
             lambda: ([Optional[int]], Optional[int])),
            ("method_with_u_int", "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f645769746855496e74", "method", None,
             lambda: ([Optional[int]], Optional[int])),
            ("method_with_long", "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f64576974684c6f6e67", "method", None,
             lambda: ([Optional[int]], Optional[int])),
            ("method_with_u_long", "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f6457697468554c6f6e67", "method", None,
             lambda: ([Optional[int]], Optional[int])),
            ("method_with_double", "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f6457697468446f75626c65", "method", None,
             lambda: ([Optional[bool]], Optional[bool])),
            ("method_with_float", "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f6457697468466c6f6174", "method", None,
             lambda: ([Optional[float]], Optional[float])),
            ("method_with_double", "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f6457697468446f75626c653a31", "method", None,
             lambda: ([Optional[float]], Optional[float])),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_ListenerWithNullable):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def method_with_byte(self, input: Optional[int]) -> Optional[int]:
        return _wrap(generated.smoke_ListenerWithNullable.method_with_byte(self, _unwrap(input, Optional[int])), Optional[int])

    def method_with_u_byte(self, input: Optional[int]) -> Optional[int]:
        return _wrap(generated.smoke_ListenerWithNullable.method_with_u_byte(self, _unwrap(input, Optional[int])), Optional[int])

    def method_with_short(self, input: Optional[int]) -> Optional[int]:
        return _wrap(generated.smoke_ListenerWithNullable.method_with_short(self, _unwrap(input, Optional[int])), Optional[int])

    def method_with_u_short(self, input: Optional[int]) -> Optional[int]:
        return _wrap(generated.smoke_ListenerWithNullable.method_with_u_short(self, _unwrap(input, Optional[int])), Optional[int])

    def method_with_int(self, input: Optional[int]) -> Optional[int]:
        return _wrap(generated.smoke_ListenerWithNullable.method_with_int(self, _unwrap(input, Optional[int])), Optional[int])

    def method_with_u_int(self, input: Optional[int]) -> Optional[int]:
        return _wrap(generated.smoke_ListenerWithNullable.method_with_u_int(self, _unwrap(input, Optional[int])), Optional[int])

    def method_with_long(self, input: Optional[int]) -> Optional[int]:
        return _wrap(generated.smoke_ListenerWithNullable.method_with_long(self, _unwrap(input, Optional[int])), Optional[int])

    def method_with_u_long(self, input: Optional[int]) -> Optional[int]:
        return _wrap(generated.smoke_ListenerWithNullable.method_with_u_long(self, _unwrap(input, Optional[int])), Optional[int])

    def method_with_double(self, *args, **kwargs) -> Optional[bool]:
        return _wrap(generated.smoke_ListenerWithNullable.method_with_double(self, *[_unwrap(a) for a in args], **{k: _unwrap(v) for k, v in kwargs.items()}), Optional[bool])

    def method_with_float(self, input: Optional[float]) -> Optional[float]:
        return _wrap(generated.smoke_ListenerWithNullable.method_with_float(self, _unwrap(input, Optional[float])), Optional[float])



