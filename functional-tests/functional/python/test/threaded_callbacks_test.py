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

"""Threaded native calls and Python callbacks finish within bounded subprocesses."""

import subprocess
import sys
import pytest

SETUP = '''
import threading
import functional
from test.ThreadedListener import ThreadedListener
from test.ThreadedNotifier import ThreadedNotifier
from test.UnloadedClass import UnloadedClass

class Listener(ThreadedListener):
    def __init__(self):
        super().__init__()
        self.messages = []
        self.unloaded_values = []

    def unloaded(self, value):
        assert isinstance(value, UnloadedClass)
        assert value.increment(41) == 42
        self.unloaded_values.append(value)

    def on_event(self, message):
        self.messages.append(message)
        return len(message)

notifier = ThreadedNotifier.create_on_new_thread()
listener = Listener()
'''


def run_threaded_case(code):
    result = subprocess.run([sys.executable, '-c', SETUP + code], capture_output=True, text=True, timeout=20)
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize('adopted', [False, True])
def test_native_worker_join_releases_gil_and_allows_reentrant_calls(adopted):
    code = '''
assert notifier.notify(listener, 'worker') == 6
assert listener.messages == ['worker']
assert len(listener.unloaded_values) == 1
'''
    if adopted:
        code = '''
dispatcher = ThreadedNotifier.create_dispatcher()
adopted = functional.test_ThreadedDispatcher(dispatcher._native)
assert adopted.notify(listener, 'worker') == 6
assert listener.messages == ['worker']
assert len(listener.unloaded_values) == 1
'''
    run_threaded_case(code)


def test_detached_interface_and_lambda_finish_before_shutdown():
    run_threaded_case('''
seen = []
def callback(message):
    seen.append(message)
notifier.notify_on_detached(listener, 'interface')
notifier.notify_lambda_on_detached(callback, 'lambda')
notifier.wait_for_callbacks()
assert listener.messages == ['interface']
assert seen == ['lambda']
''')


def test_concurrent_native_calls_allow_worker_callbacks():
    run_threaded_case('''
from concurrent.futures import ThreadPoolExecutor
listeners = [Listener() for _ in range(4)]
with ThreadPoolExecutor(max_workers=4) as pool:
    futures = [pool.submit(notifier.notify, item, 'parallel') for item in listeners]
    assert [future.result(timeout=10) for future in futures] == [8] * 4
assert all(item.messages == ['parallel'] for item in listeners)
assert all(len(item.unloaded_values) == 1 for item in listeners)
''')


@pytest.mark.parametrize('detached', [False, True])
def test_native_worker_callback_errors_follow_native_exception_policy(detached):
    run_threaded_case('''
class ThrowingListener(Listener):
    def on_event(self, message):
        raise ValueError('worker callback failed')
throwing = ThrowingListener()
try:
    if DETACHED:
        notifier.notify_on_detached(throwing, 'error')
        notifier.wait_for_callbacks()
    else:
        notifier.notify(throwing, 'error')
except ValueError as error:
    assert str(error) == 'worker callback failed'
else:
    raise AssertionError('worker exception was lost')
'''.replace('DETACHED', str(detached)))


def test_detached_error_waits_for_all_callbacks_before_shutdown():
    run_threaded_case('''
class ThrowingListener(Listener):
    def on_event(self, message):
        raise ValueError('worker callback failed')
throwing = ThrowingListener()
seen = []
notifier.notify_on_detached(throwing, 'error')
notifier.notify_lambda_on_detached(lambda message: seen.append(message), 'completed')
try:
    notifier.wait_for_callbacks()
except ValueError as error:
    assert str(error) == 'worker callback failed'
else:
    raise AssertionError('worker exception was lost')
assert seen == ['completed']
''')


@pytest.mark.parametrize('path', ['method', 'optional', 'collection', 'field', 'field_collection', 'property', 'throwing'])
def test_returned_native_callable_releases_gil_for_worker_join(path):
    run_threaded_case('''
path = PATH
if path == 'method':
    callback = ThreadedNotifier.get_worker_callback()
elif path == 'optional':
    assert ThreadedNotifier.get_nullable_worker_callback(False) is None
    callback = ThreadedNotifier.get_nullable_worker_callback(True)
elif path == 'collection':
    callbacks = ThreadedNotifier.get_worker_callbacks()
    assert callbacks[1] is None
    callback = callbacks[0]
elif path == 'field':
    callback = ThreadedNotifier.get_callback_holder().callback
elif path == 'field_collection':
    holder = ThreadedNotifier.get_callback_holder()
    assert holder.callbacks[1] is None
    callback = holder.callbacks[0]
elif path == 'property':
    callback = ThreadedNotifier.worker_operation()
else:
    callback = ThreadedNotifier.get_throwing_callback()
assert callback(listener, 'worker') == 6
assert listener.messages == ['worker']
'''.replace('PATH', repr(path)))


@pytest.mark.parametrize('property_setter', [False, True])
def test_callback_argument_native_callable_releases_gil(property_setter):
    run_threaded_case('''
from test.ThreadedCallableListener import ThreadedCallableListener
class Receiver(ThreadedCallableListener):
    def __init__(self):
        super().__init__()
        self.result = None
    def accept(self, callback):
        return callback(listener, 'worker')
    @property
    def callback(self):
        return None
    @callback.setter
    def callback(self, callback):
        self.result = callback(listener, 'worker')
receiver = Receiver()
if PROPERTY:
    ThreadedNotifier.set_callback(receiver)
    assert receiver.result == 6
else:
    assert ThreadedNotifier.send_callback(receiver) == 6
assert listener.messages == ['worker']
'''.replace('PROPERTY', str(property_setter)))
