


from _native_base import _NativeBase


class MixedCollectionsStruct(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    almost_dates: list[Optional[datetime.datetime]]


    dates: list[datetime.datetime]

