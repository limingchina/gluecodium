

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
#include "fire/SomeStruct.h"
#include "smoke/ConstantDefaults.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ConstantDefaults = ::smoke::ConstantDefaults;

void register_smoke_ConstantDefaults(py::module_& module) {
    py::class_<ConstantDefaults>(module, "smoke_ConstantDefaults")
        .def_readwrite("field1", &ConstantDefaults::field1)
        .def_readwrite("field2", &ConstantDefaults::field2)
        .def(py::init<>())
        .def(py::init<::fire::SomeStruct, ::fire::SomeStruct>(), py::arg("field1"), py::arg("field2"))
        .def(py::init<::fire::SomeStruct, ::fire::SomeStruct>(), py::arg("field1"), py::arg("field2"))
        ;
}

