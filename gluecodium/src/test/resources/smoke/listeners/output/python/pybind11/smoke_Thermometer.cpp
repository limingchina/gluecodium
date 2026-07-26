

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

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


void register_smoke_Thermometer(py::module_& module) {
    py::class_<Thermometer, std::shared_ptr<Thermometer>>(module, "smoke_Thermometer")
        .def_static("make_with_duration", [](const ::std::chrono::seconds interval, py::handle observers) {
                return Thermometer::make_with_duration(interval, gluecodium::python::from_python_regular<::std::vector< ::std::shared_ptr< ::smoke::TemperatureObserver > >>(observers));
            }, py::arg("interval"), py::arg("observers"))
        .def_static("make_without_duration", [](py::handle observers) {
                return Thermometer::make_without_duration(gluecodium::python::from_python_regular<::std::vector< ::std::shared_ptr< ::smoke::TemperatureObserver > >>(observers));
            }, py::arg("observers"))
        .def_static("throwing_make", [](const int32_t id, py::handle observers) {
                return Thermometer::throwing_make(id, gluecodium::python::from_python_regular<::std::vector< ::std::shared_ptr< ::smoke::TemperatureObserver > >>(observers));
            }, py::arg("id"), py::arg("observers"))
        .def_static("nothrow_make", [](const ::std::string& label, py::handle nice_observers) {
                return Thermometer::nothrow_make(label, gluecodium::python::from_python_regular<::std::vector< ::std::shared_ptr< ::smoke::TemperatureObserver > >>(nice_observers));
            }, py::arg("label"), py::arg("nice_observers"))
        .def_static("another_throwing_make", [](const bool dummy, py::handle observers) {
                return Thermometer::another_throwing_make(dummy, gluecodium::python::from_python_regular<::std::vector< ::std::shared_ptr< ::smoke::TemperatureObserver > >>(observers));
            }, py::arg("dummy"), py::arg("observers"))
                .def_static("notify_observers", [](const ::std::shared_ptr< ::smoke::Thermometer >& thermometer, py::handle some_observers) {
                        Thermometer::notify_observers(thermometer, gluecodium::python::from_python_regular<::std::vector< ::std::shared_ptr< ::smoke::TemperatureObserver > >>(some_observers));
                }, py::arg("thermometer"), py::arg("some_observers"))
                .def_static("throwing_notify_observers", [](const ::std::shared_ptr< ::smoke::Thermometer >& thermometer, py::handle some_observers) {
                        return Thermometer::throwing_notify_observers(thermometer, gluecodium::python::from_python_regular<::std::vector< ::std::shared_ptr< ::smoke::TemperatureObserver > >>(some_observers));
                }, py::arg("thermometer"), py::arg("some_observers"))
        .def("force_update", &Thermometer::force_update)
        .def("get_celsius", &Thermometer::get_celsius)
        .def("get_kelvin", &Thermometer::get_kelvin)
        .def("get_fahrenheit", &Thermometer::get_fahrenheit)
        ;
}

