# Copyright (C) 2016-2026 HERE Europe B.V.
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

"""Public callback conversions through native method, property and callable boundaries."""

from test.ForecastFactory import ForecastFactory
from test.ForecastListener import ForecastListener
from test.ForecastData import ForecastData


def test_callback_map_arguments_are_public_structs():
    captured = []

    class Listener(ForecastListener):
        def on_forecast_data_provided(self, data):
            assert data
            assert all(isinstance(value, ForecastData) for value in data.values())
            captured.append(data)

    listener = Listener()
    ForecastFactory.create_provider().inform(listener)
    assert captured


# These calls are initiated in C++; direct calls to user overrides retain normal Python semantics.
from test.DerivedPublicStructuredCallback import DerivedPublicStructuredCallback
from test.PublicCallbackContract import PublicCallbackContract
from test.NullablePayload import NullablePayload
from test.ListenerWithAttributes import ListenerWithAttributes
from test.AttributedMessageDelivery import AttributedMessageDelivery
from test.ListenerWithReturn import ListenerWithReturn
import pytest


class StructuredListener(DerivedPublicStructuredCallback):
    def __init__(self):
        super().__init__()
        self.value = None
        self.expected = None
        self.invocations = 0

    def round_trip(self, values):
        assert values["values"][0] is self.expected
        assert values["values"][1] is None
        self.invocations += 1
        return values

    @property
    def payload(self):
        return self.value

    @payload.setter
    def payload(self, value):
        assert value is None or isinstance(value, NullablePayload)
        self.value = value


@pytest.mark.parametrize("nullable", [False, True])
def test_inherited_callback_nested_collection_identity(nullable):
    listener = StructuredListener()
    value = None if nullable else NullablePayload.create()
    listener.expected = value
    assert PublicCallbackContract.invoke(listener, value) == {"values": [value, None]}
    assert listener.invocations == 1
    # No adapters are inserted into the public method itself.
    values = {"values": [value, None]}
    assert listener.round_trip(values) is values


@pytest.mark.parametrize("nullable", [False, True])
def test_public_property_callback_wrappers(nullable):
    listener = StructuredListener()
    value = None if nullable else NullablePayload.create()
    assert PublicCallbackContract.property_round_trip(listener, value) is value
    assert listener.payload is value


def test_legacy_property_callback_public_struct():
    seen = []

    class Listener(ListenerWithAttributes):
        def set_structured_message(self, value):
            assert isinstance(value, ListenerWithReturn.MessageStruct)
            seen.append(value)

        def get_structured_message(self):
            return seen[-1]

    listener = Listener()
    assert AttributedMessageDelivery.create().check_structured_message_round_trip(listener)
    assert seen


@pytest.mark.parametrize("nullable", [False, True])
def test_lambda_callback_public_arguments_and_return(nullable):
    value = None if nullable else NullablePayload.create()
    seen = []

    def callback(argument):
        assert argument is value
        seen.append(argument)
        return argument

    assert PublicCallbackContract.invoke_lambda(callback, value) is value
    assert seen == [value]
    assert callback(value) is value


@pytest.mark.parametrize("nullable", [False, True])
def test_native_lambda_accepts_and_returns_public_wrappers(nullable):
    value = None if nullable else NullablePayload.create()
    callback = PublicCallbackContract.get_lambda()
    assert callback(value) is value


@pytest.mark.parametrize("keywords", [False, True])
def test_struct_constructor_lambda_uses_typed_conversion(keywords):
    value = NullablePayload.create()

    def callback(argument):
        assert argument is value
        return argument

    holder_type = PublicCallbackContract.CallbackHolder
    holder = holder_type(callback=callback) if keywords else holder_type(callback)
    assert PublicCallbackContract.invoke_holder(holder, value) is value
    assert holder.callback(value) is value


def test_callback_exception_propagates_to_python_caller():
    class FailingListener(StructuredListener):
        def round_trip(self, values):
            raise ValueError("callback failure")

    with pytest.raises(ValueError, match="callback failure"):
        PublicCallbackContract.invoke(FailingListener(), None)


def test_throwing_interface_successful_public_override():
    from test.ErrorsInInterface import ErrorsInInterface
    from test.ErrorMessenger import ErrorMessenger

    class Listener(ErrorsInInterface):
        def get_message(self):
            return "callback succeeds"

        def set_message(self, value):
            assert value == "callback input"

        def get_message_with_payload(self):
            return "payload callback succeeds"

        def set_message_with_payload(self, value):
            assert value == "payload callback input"

    listener = Listener()
    messenger = ErrorMessenger.create()
    assert messenger.get_message(listener) == "callback succeeds"
    messenger.set_message(listener, "callback input")
    assert messenger.get_message_with_payload(listener) == "payload callback succeeds"
    messenger.set_message_with_payload(listener, "payload callback input")


def test_native_lambda_does_not_discard_extra_arguments():
    callback = PublicCallbackContract.get_lambda()
    with pytest.raises(TypeError):
        callback(None, None)


def test_lambda_parameter_rejects_noncallable():
    with pytest.raises(TypeError):
        PublicCallbackContract.invoke_lambda("not a callback", None)


def test_field_constructor_overloads_preserve_callable_types():
    value = NullablePayload.create()
    seen = []

    def callback(argument):
        assert argument is value
        seen.append(argument)
        return argument

    holder_type = PublicCallbackContract.CallbackChoice
    integer_holder = holder_type(42)
    assert integer_holder.integer == 42
    assert integer_holder.callback is None
    holder = holder_type(callback)
    assert holder.integer == 0
    assert PublicCallbackContract.invoke_lambda(holder.callback, value) is value
    assert seen == [value]


@pytest.mark.parametrize("base", ["PublicStructuredCallback", "DerivedPublicStructuredCallback"])
def test_property_setter_override_does_not_bridge_inherited_generated_getter(base):
    import subprocess
    import sys

    code = f"""
from test.PublicStructuredCallback import PublicStructuredCallback
from test.DerivedPublicStructuredCallback import DerivedPublicStructuredCallback
from test.PublicCallbackContract import PublicCallbackContract
class SetterOnly({base}):
    @PublicStructuredCallback.payload.setter
    def payload(self, value):
        self.value = value
try:
    PublicCallbackContract.property_round_trip(SetterOnly(), None)
except RuntimeError as error:
    assert "pure virtual" in str(error), str(error)
else:
    raise AssertionError("missing getter override must be reported")
"""
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=5)
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("descriptor", [staticmethod, classmethod])
def test_callback_static_and_class_method_overrides_use_public_wrappers(descriptor):
    from test.ListenerWithReturn import ListenerWithReturn
    from test.MessageDelivery import MessageDelivery

    class Listener(ListenerWithReturn):
        @descriptor
        def get_structured_message(*args):
            if descriptor is classmethod:
                assert args == (Listener,)
            else:
                assert args == ()
            return ListenerWithReturn.MessageStruct("Works")

    assert MessageDelivery.create_me().get_structured_message(Listener()) == "Works"


def test_callback_override_decorated_with_base_signature_is_not_forwarding_stub():
    import functools
    from test.ListenerWithReturn import ListenerWithReturn
    from test.MessageDelivery import MessageDelivery

    class Listener(ListenerWithReturn):
        @functools.wraps(ListenerWithReturn.get_structured_message)
        def get_structured_message(self):
            return ListenerWithReturn.MessageStruct("Works")

    assert MessageDelivery.create_me().get_structured_message(Listener()) == "Works"


@pytest.mark.parametrize("nullable", [False, True])
def test_inherited_callback_callable_hints(nullable):
    value = None if nullable else NullablePayload.create()

    class Listener(DerivedPublicStructuredCallback):
        def on_lambda(self, callback, argument):
            assert argument is value
            assert callback(argument) is value
            return callback(argument)

    listener = Listener()
    assert PublicCallbackContract.invoke_inherited_lambda(listener, value) is value
    callback = lambda argument: argument
    assert listener.on_lambda(callback, value) is value
