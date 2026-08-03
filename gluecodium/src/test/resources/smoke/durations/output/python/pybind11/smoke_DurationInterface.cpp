

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
#include "smoke/DurationInterface.h"
#include "chrono"
#include "string"

using DurationInterface = ::smoke::DurationInterface;

class DurationInterfaceTrampoline : public DurationInterface {
public:
    using DurationInterface::DurationInterface;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<DurationInterface> m_impl;

    ::std::string duration_function(
            ::std::chrono::seconds input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->duration_function(input);
        }
        PYBIND11_OVERRIDE_PURE(::std::string, DurationInterface, duration_function, input);
    }
};



void register_smoke_DurationInterface(py::module_& module) {
auto cls_DurationInterface = py::class_<DurationInterface, std::shared_ptr<DurationInterface>, DurationInterfaceTrampoline>(module, "smoke_DurationInterface")
        .def("__gluecodium_id__", [](const DurationInterface& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<DurationInterface> native) {
            auto self = std::make_shared<DurationInterfaceTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("duration_function", [](DurationInterface& self, const ::std::chrono::seconds input) {
            return self.duration_function(input);
        }, py::arg("input"))
        ;


}
