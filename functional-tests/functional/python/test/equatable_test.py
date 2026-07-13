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

"""Equatable mapping tests for the Python (pybind11) bindings."""

import functional
from test.equatable import EquatableClass, Equatable

import pytest


class TestEquatable:
    def test_are_equal(self):
        a = EquatableClass()
        b = EquatableClass()

        assert EquatableClass.are_equal(a, b) is True

    def test_not_equal(self):
        a = EquatableClass()
        b = EquatableClass()

        assert EquatableClass.are_equal(a, b) is True

    def test_struct_equality(self):
        a = Equatable(field1="x", field2=1)
        b = Equatable(field1="x", field2=1)

        assert a == b
