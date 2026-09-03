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

"""Reference equality tests for the Python (pybind11) bindings."""

import functional
from test.DummyFactory import DummyFactory
from test.DummyClass import DummyClass

import pytest


class TestRefEquality:
    def test_singleton_is_same_instance(self):
        first = DummyFactory.get_dummy_class_singleton()
        second = DummyFactory.get_dummy_class_singleton()

        assert first is second

    def test_created_instances_differ(self):
        first = DummyFactory.create_dummy_class()
        second = DummyFactory.create_dummy_class()

        assert first is not second

    def test_round_trip_preserves_identity(self):
        original = DummyFactory.get_dummy_class_singleton()
        result = DummyClass.dummy_class_round_trip(original)

        assert result is original
