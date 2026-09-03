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

"""Complex listener (callback) tests for the Python (pybind11) bindings.

Tests complex callback patterns: a listener interface with a method that
receives multiple complex parameters (a class instance, a list of structs,
an enum, and a Blob), and a notifier that triggers the callback from C++.
"""

import functional
from test.ComplexListener import ComplexListener
from test.ComplexListenerFactory import ComplexListenerFactory
from test.NamedPoint3D import NamedPoint3D
from test.Point3D import Point3D
from test.TrajectoryQuality import TrajectoryQuality

import pytest


IMAGE = (
    b"      _.-'''''-._      \n"
    b"    .'  _     _  '.    \n"
    b"   /   (o)   (o)   \\  \n"
    b"  |                 |  \n"
    b"  |  \\          /  |  \n"
    b"  \\  '.       .'  /   \n"
    b"    '.  `'---'`  .'    \n"
    b"      '-._____.-'"
)


class TestComplexListeners:
    def test_python_native_listener_with_complex_input_parameters(self):
        """A Python subclass of ComplexListener receives a callback from C++ with
        complex parameters: a DistanceMetric instance, a list of NamedPoint3D
        structs, a TrajectoryQuality enum, and a Blob (bytes)."""
        pt_one = NamedPoint3D("zero point", Point3D())
        pt_two = NamedPoint3D("intermediate point", Point3D(10.0, 10.0, 10.0))
        pt_three = NamedPoint3D("final destination", Point3D(20.0, 20.0, 20.0))
        trajectory = [pt_one, pt_two, pt_three]

        listener_log = {}

        class PythonComplexListener(ComplexListener):
            def __init__(self):
                super().__init__()

            def on_trajectory_completed(self, distance_metric, traj, quality, image):
                length = distance_metric.get_length(traj)
                listener_log["from"] = traj[0].name
                listener_log["to"] = traj[-1].name
                listener_log["quality"] = quality
                listener_log["length"] = length
                listener_log["image"] = image

        listener = PythonComplexListener()
        notifier = ComplexListenerFactory.create_complex_notifier()
        notifier.trajectory_completed(trajectory, TrajectoryQuality.TRAJECTORY_AVERAGE, IMAGE, listener)

        assert listener_log["from"] == "zero point"
        assert listener_log["to"] == "final destination"
        # The callback receives the native pybind11 enum value (not the Python wrapper
        # enum), so compare by .value which is the native enum.
        assert listener_log["quality"] == TrajectoryQuality.TRAJECTORY_AVERAGE.value
        # Manhattan distance: |0-10|*3 + |10-20|*3 = 30 + 30 = 60
        assert listener_log["length"] == 60.0
        assert listener_log["image"] == IMAGE

    def test_distance_metric_from_factory(self):
        """ComplexListenerFactory.create_distance_metric returns a DistanceMetric
        whose get_length computes the Manhattan distance correctly."""
        metric = ComplexListenerFactory.create_distance_metric()
        pt_one = NamedPoint3D("a", Point3D(0.0, 0.0, 0.0))
        pt_two = NamedPoint3D("b", Point3D(3.0, 4.0, 0.0))
        # Manhattan: |0-3| + |0-4| + |0-0| = 7
        assert metric.get_length([pt_one, pt_two]) == 7.0

    def test_listener_receives_correct_trajectory_data(self):
        """Verify that the trajectory list received in the callback has the
        correct struct field values (Point3D coordinates and names)."""
        pt_one = NamedPoint3D("start", Point3D(1.0, 2.0, 3.0))
        pt_two = NamedPoint3D("end", Point3D(4.0, 5.0, 6.0))
        trajectory = [pt_one, pt_two]

        received = {}

        class TrajectoryChecker(ComplexListener):
            def __init__(self):
                super().__init__()

            def on_trajectory_completed(self, distance_metric, traj, quality, image):
                received["count"] = len(traj)
                received["first"] = traj[0]
                received["last"] = traj[-1]

        listener = TrajectoryChecker()
        notifier = ComplexListenerFactory.create_complex_notifier()
        notifier.trajectory_completed(trajectory, TrajectoryQuality.TRAJECTORY_GOOD, b"", listener)

        assert received["count"] == 2
        assert received["first"].name == "start"
        assert received["first"].pt.x == 1.0
        assert received["first"].pt.y == 2.0
        assert received["first"].pt.z == 3.0
        assert received["last"].name == "end"
        assert received["last"].pt.x == 4.0
        assert received["last"].pt.y == 5.0
        assert received["last"].pt.z == 6.0

    def test_listener_with_all_quality_values(self):
        """Test that all TrajectoryQuality enum values are correctly passed
        through the callback."""
        for quality in [
            TrajectoryQuality.TRAJECTORY_POOR,
            TrajectoryQuality.TRAJECTORY_AVERAGE,
            TrajectoryQuality.TRAJECTORY_GOOD,
        ]:
            received_quality = {}

            class QualityChecker(ComplexListener):
                def __init__(self):
                    super().__init__()

                def on_trajectory_completed(self, distance_metric, traj, q, image):
                    received_quality["value"] = q

            listener = QualityChecker()
            notifier = ComplexListenerFactory.create_complex_notifier()
            trajectory = [NamedPoint3D("a", Point3D())]
            notifier.trajectory_completed(trajectory, quality, b"", listener)

            # The callback receives the native pybind11 enum (not the Python wrapper enum).
            assert received_quality["value"] == quality.value
