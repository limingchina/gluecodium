# Copyright (C) 2016-2025 HERE Europe B.V.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# License-Filename: LICENSE

"""Date mapping tests for the Python (pybind11) bindings."""

import datetime

import functional
from test.dates import Dates

import pytest


class TestDates:
    def test_increase_date(self):
        input_date = datetime.datetime(2020, 1, 1, 0, 0, 0)
        result = Dates.increase_date(input_date)

        # increaseDate adds one day, hour, minute and second.
        assert result == datetime.datetime(2020, 1, 2, 1, 1, 1)

    def test_increase_date_maybe(self):
        input_date = datetime.datetime(2021, 6, 1, 0, 0, 0)
        result = Dates.increase_date_maybe(input_date)

        assert result is not None
        assert result == datetime.datetime(2021, 6, 2, 1, 1, 1)

    def test_increase_date_maybe_null(self):
        result = Dates.increase_date_maybe(None)

        assert result is None
