

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
#include "smoke/TemperatureObserver.h"
#include "smoke/Thermometer.h"
#include "memory"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using TemperatureObserver = ::smoke::TemperatureObserver;

class TemperatureObserverTrampoline : public TemperatureObserver {
public:
    using TemperatureObserver::TemperatureObserver;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<TemperatureObserver> m_impl;

    void on_temperature_update(
            const ::std::shared_ptr< ::smoke::Thermometer >& thermometer ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->on_temperature_update(thermometer);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, TemperatureObserver, on_temperature_update, thermometer);
    }
};

void register_smoke_TemperatureObserver(py::module_& module) {
    py::class_<TemperatureObserver, std::shared_ptr<TemperatureObserver>, TemperatureObserverTrampoline>(module, "smoke_TemperatureObserver")
        .def("__gluecodium_id__", [](const TemperatureObserver& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<TemperatureObserver> native) {
            auto self = std::make_shared<TemperatureObserverTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("on_temperature_update", [](TemperatureObserver& self, const ::std::shared_ptr< ::smoke::Thermometer >& thermometer) {
            return self.on_temperature_update(thermometer);
        }, py::arg("thermometer"))
        ;
}

