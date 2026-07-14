

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/DurationHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/TemperatureObserver.h"
#include "smoke/Thermometer.h"
#include "chrono"
#include "cstdint"
#include "memory"
#include "string"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Thermometer = ::smoke::Thermometer;

void register_Thermometer(py::module_& module) {
    py::class_<Thermometer, std::shared_ptr<Thermometer>>(module, "Thermometer")
        .def_static("make_with_duration", &Thermometer::make_with_duration, py::arg("interval"), py::arg("observers"))
        .def_static("make_without_duration", &Thermometer::make_without_duration, py::arg("observers"))
        .def_static("throwing_make", &Thermometer::throwing_make, py::arg("id"), py::arg("observers"))
        .def_static("nothrow_make", &Thermometer::nothrow_make, py::arg("label"), py::arg("nice_observers"))
        .def_static("another_throwing_make", &Thermometer::another_throwing_make, py::arg("dummy"), py::arg("observers"))
        .def_static("notify_observers", &Thermometer::notify_observers, py::arg("thermometer"), py::arg("some_observers"))
        .def_static("throwing_notify_observers", &Thermometer::throwing_notify_observers, py::arg("thermometer"), py::arg("some_observers"))
        .def("force_update", &Thermometer::force_update)
        .def("get_celsius", &Thermometer::get_celsius)
        .def("get_kelvin", &Thermometer::get_kelvin)
        .def("get_fahrenheit", &Thermometer::get_fahrenheit)
        ;
}

