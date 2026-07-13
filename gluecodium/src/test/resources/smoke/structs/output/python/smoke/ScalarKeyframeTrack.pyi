


from _native_base import _NativeBase


class ScalarKeyframeTrack(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    keyframes: list[ScalarKeyframe]


    easing_function: str


    interpolation_mode: str

