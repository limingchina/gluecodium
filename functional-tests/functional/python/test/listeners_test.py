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

"""Listener (callback) tests for the Python (pybind11) bindings.

Tests basic listener/callback patterns: a Python subclass of a listener
interface receives a callback from C++ through the pybind11 trampoline.
Covers the MultiListener, StringListeners, ListenerRoundtrip, and
ListenerWithMaps features.
"""

import functional
from test.MultiSender import MultiSender
from test.ReceiverA import ReceiverA
from test.ReceiverB import ReceiverB
from test.DummyLogger import DummyLogger
from test.StringListener import StringListener
from test.PersistingLogger import PersistingLogger
from test.SomeSimpleInterface import SomeSimpleInterface
from test.SomeSimpleRoundTrip import SomeSimpleRoundTrip
from test.ForecastFactory import ForecastFactory
from test.ForecastListener import ForecastListener
from test.ForecastData import ForecastData

import pytest


class TestMultiListener:
    """Tests for MultiSender notifying Receiver_A and Receiver_B listeners."""

    def test_receiver_a_notification(self):
        """A Python subclass of Receiver_A receives a callback from C++ when
        MultiSender.notify_a_receivers() is called."""
        received = []

        class _ReceiverA(ReceiverA):
            def __init__(self):
                super().__init__()

            def receive_a(self, message: str):
                received.append(message)

        sender = MultiSender.create()
        receiver = _ReceiverA()
        sender.add_receiver_a(receiver)
        sender.notify_a_receivers()

        assert received == ["Sent from A"]

    def test_receiver_b_notification(self):
        """A Python subclass of Receiver_B receives a callback from C++ when
        MultiSender.notify_b_receivers() is called."""
        received = []

        class _ReceiverB(ReceiverB):
            def __init__(self):
                super().__init__()

            def receive_b(self, message: str):
                received.append(message)

        sender = MultiSender.create()
        receiver = _ReceiverB()
        sender.add_receiver_b(receiver)
        sender.notify_b_receivers()

        assert received == ["Sent from B"]

    def test_multiple_receivers_a(self):
        """Multiple Receiver_A listeners all receive the notification."""
        received_a = []
        received_b = []

        class _ReceiverA(ReceiverA):
            def __init__(self):
                super().__init__()

            def receive_a(self, message: str):
                received_a.append(message)

        class _ReceiverB(ReceiverB):
            def __init__(self):
                super().__init__()

            def receive_b(self, message: str):
                received_b.append(message)

        sender = MultiSender.create()
        sender.add_receiver_a(_ReceiverA())
        sender.add_receiver_a(_ReceiverA())
        sender.add_receiver_b(_ReceiverB())
        sender.notify_a_receivers()
        sender.notify_b_receivers()

        assert len(received_a) == 2
        assert all(msg == "Sent from A" for msg in received_a)
        assert received_b == ["Sent from B"]


class TestStringListeners:
    """Tests for DummyLogger and PersistingLogger relay patterns."""

    def test_relay_message(self):
        """DummyLogger.relay_message calls onMessage on the listener."""
        received = []

        class _Listener(StringListener):
            def __init__(self):
                super().__init__()

            def on_message(self, message: str):
                received.append(message)

            def on_struct_message(self, message):
                pass

            def on_const_message(self, message: str):
                pass

        DummyLogger.relay_message(_Listener(), "Hi!")
        assert received == ["Hi!"]

    def test_relay_const_message(self):
        """DummyLogger.relay_const_message calls onConstMessage on the listener."""
        received = []

        class _Listener(StringListener):
            def __init__(self):
                super().__init__()

            def on_message(self, message: str):
                pass

            def on_struct_message(self, message):
                pass

            def on_const_message(self, message: str):
                received.append(message)

        DummyLogger.relay_const_message(_Listener(), "Hi!")
        assert received == ["Hi!"]

    def test_persisting_logger_add_and_remove(self):
        """PersistingLogger.addListener / removeListener / messageAll work."""
        received = []

        class _Listener(StringListener):
            def __init__(self):
                super().__init__()

            def on_message(self, message: str):
                received.append(message)

            def on_struct_message(self, message):
                pass

            def on_const_message(self, message: str):
                pass

        listener = _Listener()
        PersistingLogger.add_listener(listener)
        PersistingLogger.message_all("Hello")
        assert received == ["Hello"]

        # After removal, the listener should not receive further messages.
        assert PersistingLogger.remove_listener(listener) is True
        PersistingLogger.message_all("World")
        assert received == ["Hello"]

        PersistingLogger.remove_all_listeners()


class TestListenerRoundtrip:
    """Tests for SomeSimpleRoundTrip interface round-trip."""

    def test_simple_round_trip(self):
        """SomeSimpleRoundTrip.round_trip returns the same interface instance
        back to C++ and the property value is preserved."""
        class _SimpleInterface(SomeSimpleInterface):
            def __init__(self):
                super().__init__()

            def get_value(self) -> str:
                return "this is a value"

        instance = _SimpleInterface()
        result = SomeSimpleRoundTrip.round_trip(instance)

        assert result.value == "this is a value"


class TestListenerWithMaps:
    """Tests for ForecastListener receiving a Map parameter."""

    def test_python_listener_receives_map(self):
        """A Python subclass of ForecastListener receives a Map<String, ForecastData>
        from C++ through the trampoline."""
        received_data = {}

        class _ForecastListener(ForecastListener):
            def __init__(self):
                super().__init__()

            def on_forecast_data_provided(self, data):
                for city, forecast in data.items():
                    received_data[city] = (forecast.lowest_degree, forecast.highest_degree)

        provider = ForecastFactory.create_provider()
        listener = _ForecastListener()
        provider.inform(listener)

        assert "Berlin" in received_data
        assert received_data["Berlin"] == (-2, 26)
        assert "Madrid" in received_data
        assert received_data["Madrid"] == (1, 33)
        assert "Marrakesh" in received_data
        assert received_data["Marrakesh"] == (8, 40)
