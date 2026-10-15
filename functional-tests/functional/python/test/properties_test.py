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

"""Property mapping tests for the Python (pybind11) bindings."""

import functional
from test.Attributes import Attributes

import pytest


class TestProperties:
    def test_readonly_attribute(self):
        attributes = Attributes.create()

        assert attributes.readonly_attribute is not None

    def test_readwrite_attribute(self):
        attributes = Attributes.create()
        attributes.built_in_type_attribute = 42

        assert attributes.built_in_type_attribute == 42

    def test_static_attribute(self):
        Attributes.static_attribute = "static-value"

        assert Attributes.static_attribute == "static-value"
