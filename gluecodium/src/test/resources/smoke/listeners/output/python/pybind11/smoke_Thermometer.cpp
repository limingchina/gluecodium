

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/DurationHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/TemperatureObserver.h"
#include "smoke/Thermometer.h"
#include "chrono"
#include "cstdint"
#include "memory"
#include "string"
#include "vector"

void register_Thermometer(py::module_& module) {
    py::class_<Thermometer>(module, "Thermometer")
        .def("make_with_duration", &Thermometer::make_with_duration, py::arg("interval"), py::arg("observers"))
        .def("make_without_duration", &Thermometer::make_without_duration, py::arg("observers"))
        .def("throwing_make", &Thermometer::throwing_make, py::arg("id"), py::arg("observers"))
        .def("nothrow_make", &Thermometer::nothrow_make, py::arg("label"), py::arg("nice_observers"))
        .def("another_throwing_make", &Thermometer::another_throwing_make, py::arg("dummy"), py::arg("observers"))
        .def("notify_observers", &Thermometer::notify_observers, py::arg("thermometer"), py::arg("some_observers"))
        .def("throwing_notify_observers", &Thermometer::throwing_notify_observers, py::arg("thermometer"), py::arg("some_observers"))
        .def("force_update", &Thermometer::force_update)
        .def("get_celsius", &Thermometer::get_celsius)
        .def("get_kelvin", &Thermometer::get_kelvin)
        .def("get_fahrenheit", &Thermometer::get_fahrenheit)
        ;
}

