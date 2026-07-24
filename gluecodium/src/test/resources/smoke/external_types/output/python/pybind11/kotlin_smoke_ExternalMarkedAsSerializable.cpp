

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "kotlin_smoke/ExternalMarkedAsSerializable.h"
#include "cstdint"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ExternalMarkedAsSerializable = ::kotlin_smoke::ExternalMarkedAsSerializable;

void register_kotlin_smoke_ExternalMarkedAsSerializable(py::module_& module) {
    py::class_<ExternalMarkedAsSerializable>(module, "ExternalMarkedAsSerializable")
        .def_readwrite("field", &ExternalMarkedAsSerializable::field)
        .def(py::init<>())
        .def(py::init<int32_t(), py::arg("field"))
        ;
}

