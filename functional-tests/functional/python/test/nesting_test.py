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

"""Nesting mapping tests for the Python (pybind11) bindings."""

import functional
from test.nesting_in_struct import OuterStruct, InnerStruct

import pytest


class TestNesting:
    def test_nested_struct(self):
        inner = InnerStruct(value="hello")
        outer = OuterStruct(inner=inner)

        assert isinstance(outer, OuterStruct)
        assert outer.inner.value == "hello"

    def test_nested_struct_mutation(self):
        outer = OuterStruct()
        outer.inner = InnerStruct(value="world")

        assert outer.inner.value == "world"
