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

"""Listeners with attributes (interface properties) tests for the Python (pybind11) bindings.

Tests that a Python subclass of ListenerWithAttributes can override the
interface property getter/setter methods and that C++ can set and get
values through the trampoline, verifying round-trip correctness for various
types (String, struct, enum, list, map, Blob, class instances).

Key pattern: the trampoline uses PYBIND11_OVERRIDE_PURE with the C++ method
name (e.g. ``get_message``, ``set_message``).  A Python subclass overrides
those *methods* (not the Python property ``message``) so the trampoline can
discover and dispatch to them.  Getter return values and setter parameters
are native pybind11 values because the trampoline's type caster only
recognises pybind11 types.
"""

from test.ListenerWithAttributes import ListenerWithAttributes
from test.AttributedMessageDelivery import AttributedMessageDelivery

import pytest


class _TestListener(ListenerWithAttributes):
    """Python implementation of ListenerWithAttributes that stores and returns
    all values set through the setter methods, enabling round-trip tests."""

    def __init__(self):
        super().__init__()
        self._data = {}

    # --- String property ---
    def get_message(self) -> str:
        return self._data.get("message", "")

    def set_message(self, value: str):
        self._data["message"] = value

    # --- Nullable interface property ---
    def get_packed_message(self):
        return self._data.get("packed_message")

    def set_packed_message(self, value):
        self._data["packed_message"] = value

    # --- Nullable class property ---
    def get_boxed_message(self):
        return self._data.get("boxed_message")

    def set_boxed_message(self, value):
        self._data["boxed_message"] = value

    # --- Struct property ---
    def get_structured_message(self):
        return self._data.get("structured_message")

    def set_structured_message(self, value):
        self._data["structured_message"] = value

    # --- Enum property ---
    def get_enumerated_message(self):
        return self._data.get("enumerated_message")

    def set_enumerated_message(self, value):
        self._data["enumerated_message"] = value

    # --- List property ---
    def get_arrayed_message(self):
        return self._data.get("arrayed_message", [])

    def set_arrayed_message(self, value):
        self._data["arrayed_message"] = value

    # --- Map property ---
    def get_mapped_message(self):
        return self._data.get("mapped_message", {})

    def set_mapped_message(self, value):
        self._data["mapped_message"] = value

    # --- Blob property ---
    def get_buffered_message(self):
        return self._data.get("buffered_message", b"")

    def set_buffered_message(self, value):
        self._data["buffered_message"] = value


class TestListenerWithAttributes:
    def setup_method(self):
        self._envelope = _TestListener()
        self._delivery = AttributedMessageDelivery.create()

    def test_string_round_trip(self):
        assert self._delivery.check_message_round_trip(self._envelope)

    def test_package_round_trip(self):
        assert self._delivery.check_packed_message_round_trip(self._envelope)

    def test_box_round_trip(self):
        assert self._delivery.check_boxed_message_round_trip(self._envelope)

    def test_struct_round_trip(self):
        assert self._delivery.check_structured_message_round_trip(self._envelope)

    def test_enum_round_trip(self):
        assert self._delivery.check_enumerated_message_round_trip(self._envelope)

    def test_array_round_trip(self):
        assert self._delivery.check_arrayed_message_round_trip(self._envelope)

    def test_map_round_trip(self):
        assert self._delivery.check_mapped_message_round_trip(self._envelope)

    def test_blob_round_trip(self):
        assert self._delivery.check_buffered_message_round_trip(self._envelope)
