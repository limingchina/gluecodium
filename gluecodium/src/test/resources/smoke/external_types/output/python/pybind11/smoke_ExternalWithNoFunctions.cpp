

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "some/path/Bar.h"




void register_smoke_ExternalWithNoFunctions(py::module_& module) {
auto cls_ExternalWithNoFunctions = py::class_<::some::path::Bar, std::shared_ptr<::some::path::Bar>>(module, "smoke_ExternalWithNoFunctions")
        .def("__gluecodium_id__", [](const ::some::path::Bar& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<::some::path::Bar> native) {
            auto self = std::make_shared<ExternalWithNoFunctionsTrampoline>();
            self->m_impl = native;
            return self;
        }))
        ;


}
