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

"""Method overload mapping tests for the Python (pybind11) bindings."""

import functional
from test.method_overloads import MethodOverloads, Point

import pytest


class TestMethodOverloads:
    def test_is_boolean_bool(self):
        assert MethodOverloads.is_boolean(True) is True

    def test_is_boolean_int(self):
        assert MethodOverloads.is_boolean(5) is True

    def test_is_boolean_string(self):
        assert MethodOverloads.is_boolean("text") is True

    def test_is_boolean_point(self):
        assert MethodOverloads.is_boolean(Point(1.0, 2.0)) is True

    def test_is_boolean_no_args(self):
        assert MethodOverloads.is_boolean() is True
