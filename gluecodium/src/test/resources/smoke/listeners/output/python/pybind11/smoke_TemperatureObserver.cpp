

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/TemperatureObserver.h"
#include "smoke/Thermometer.h"
#include "memory"

void register_TemperatureObserver(py::module_& module) {
    py::class_<TemperatureObserver, std::shared_ptr<TemperatureObserver>>(module, "TemperatureObserver")
        .def("on_temperature_update", &TemperatureObserver::on_temperature_update, py::arg("thermometer"))
        ;
}

