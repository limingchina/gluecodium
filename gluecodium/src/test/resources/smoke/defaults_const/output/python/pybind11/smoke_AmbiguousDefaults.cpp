

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
#include "fire/AmbiguousEnum.h"
#include "fire/SomeStruct.h"
#include "smoke/AmbiguousDefaults.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using AmbiguousDefaults = ::smoke::AmbiguousDefaults;

void register_smoke_AmbiguousDefaults(py::module_& module) {
    py::class_<AmbiguousDefaults>(module, "smoke_AmbiguousDefaults")
        .def_readwrite("field1", &AmbiguousDefaults::field1)
        .def_readwrite("field2", &AmbiguousDefaults::field2)
        .def(py::init<>())
        .def(py::init<::fire::AmbiguousEnum, ::fire::SomeStruct>(), py::arg("field1"), py::arg("field2"))
        .def(py::init<::fire::AmbiguousEnum, ::fire::SomeStruct>(), py::arg("field1"), py::arg("field2"))
        ;
}

