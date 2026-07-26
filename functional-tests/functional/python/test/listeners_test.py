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

"""Listener (callback) tests for the Python (pybind11) bindings."""

import pytest

# Note: MultiListener classes are not generated for Python as documented in phase8_status.md
# Commenting out the test code until MultiListener support is added to Python bindings
#
# import functional
# from test.MultiListener import MultiSender, Receiver_A, Receiver_B


class TestListeners:
    @pytest.mark.skip(reason="MultiListener functionality is not generated for Python bindings - see phase8_status.md")
    def test_receiver_a_notification(self):
        """Test MultiSender notification to Receiver_A - currently skipped as MultiListener not available for Python"""
        pass
        # sender = MultiSender()
        # receiver = _ReceiverA()
        # sender.add_receiver_A(receiver)
        # sender.notify_A_Receivers()
        #
        # assert receiver.received


# Helper class commented out until MultiListener support is added
# class _ReceiverA(Receiver_A):
#     def __init__(self):
#         super().__init__()
#         self.received = []
#
#     def on_received(self, value: str):
#         self.received.append(value)
