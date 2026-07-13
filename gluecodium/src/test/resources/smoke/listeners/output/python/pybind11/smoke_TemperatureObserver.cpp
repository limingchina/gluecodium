

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/TemperatureObserver.h"
#include "smoke/Thermometer.h"
#include "memory"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using TemperatureObserver = ::gluecodium::smoke::TemperatureObserver;

class TemperatureObserverTrampoline : public TemperatureObserver {
public:
    using TemperatureObserver::TemperatureObserver;

    void on_temperature_update(
            const ::std::shared_ptr< ::smoke::Thermometer >& thermometer ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, TemperatureObserver, on_temperature_update, thermometer);
    }
};

void register_TemperatureObserver(py::module_& module) {
    py::class_<TemperatureObserver, std::shared_ptr<TemperatureObserver>, TemperatureObserverTrampoline>(module, "TemperatureObserver")
        .def("on_temperature_update", &TemperatureObserver::on_temperature_update, py::arg("thermometer"))
        ;
}

