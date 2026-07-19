



from _native_base import _NativeBase

import generated


class ScalarKeyframeTrack(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.ScalarKeyframeTrack):
            super().__init__(args[0])
        else:
            super().__init__(generated.ScalarKeyframeTrack(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def keyframes(self) -> list[ScalarKeyframe]:
        """"""
        return self._native.keyframes



    @property
    def easing_function(self) -> str:
        """"""
        return self._native.easing_function
    @easing_function.setter
    def easing_function(self, value: str):
      self._native.easing_function = getattr(value, "_native", value)



    @property
    def interpolation_mode(self) -> str:
        """"""
        return self._native.interpolation_mode
    @interpolation_mode.setter
    def interpolation_mode(self, value: str):
      self._native.interpolation_mode = getattr(value, "_native", value)


