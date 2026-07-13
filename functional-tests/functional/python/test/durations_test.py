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

"""Duration mapping tests for the Python (pybind11) bindings."""

import datetime

import functional
from test.durations import DurationSeconds

import pytest


class TestDurations:
    def test_increase_duration(self):
        input_duration = datetime.timedelta(seconds=10)
        result = DurationSeconds.increase_duration(input_duration)

        assert result == datetime.timedelta(seconds=11)

    def test_increase_duration_maybe(self):
        input_duration = datetime.timedelta(seconds=5)
        result = DurationSeconds.increase_duration_maybe(input_duration)

        assert result == datetime.timedelta(seconds=6)

    def test_increase_duration_maybe_null(self):
        result = DurationSeconds.increase_duration_maybe(None)

        assert result is None
