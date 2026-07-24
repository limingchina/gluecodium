

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ExternalClass.h"
#include "cstdint"
#include "memory"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using InternalOne = ::smoke::ExternalClass::InternalOne;


void register_smoke_ExternalClassInternalOne(py::module_& module) {
    py::class_<InternalOne, std::shared_ptr<InternalOne>>(module, "ExternalClassInternalOne")
        .def(py::init<>())

        .def_static("create", py::overload_cast<>(&InternalOne::create))
        .def(py::init<uint64_t>(py::arg("value")))

        .def_static("create", py::overload_cast<const uint64_t>(&InternalOne::create), py::arg("value"))
        ;
}

