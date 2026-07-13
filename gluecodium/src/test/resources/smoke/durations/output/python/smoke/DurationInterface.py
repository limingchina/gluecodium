

import datetime

class DurationInterface:
    """"""

    def __init__(self, native):
        self._native = native


    def duration_function(self, input: datetime.timedelta) -> str:
        """"""
        return self._native.duration_function(input)

