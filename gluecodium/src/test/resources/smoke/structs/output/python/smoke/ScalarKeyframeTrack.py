

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.ScalarKeyframe import ScalarKeyframe


from _native_base import _NativeBase

import generated


class ScalarKeyframeTrack(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_ScalarKeyframeTrack):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_ScalarKeyframeTrack(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def keyframes(self) -> list[ScalarKeyframe]:
        return _wrap(self._native.keyframes, list[ScalarKeyframe])


    @property
    def easing_function(self) -> str:
        return _wrap(self._native.easing_function, str)
    @easing_function.setter
    def easing_function(self, value: str):
      self._native.easing_function = _unwrap(value, str)


    @property
    def interpolation_mode(self) -> str:
        return _wrap(self._native.interpolation_mode, str)
    @interpolation_mode.setter
    def interpolation_mode(self, value: str):
      self._native.interpolation_mode = _unwrap(value, str)


