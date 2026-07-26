

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
#include "smoke/StructConstants.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using NestingStruct = ::smoke::StructConstants::NestingStruct;

void register_smoke_StructConstantsNestingStruct(py::module_& module) {
    py::class_<NestingStruct>(module, "smoke_StructConstantsNestingStruct")
        .def_readwrite("struct_field", &NestingStruct::struct_field)
        .def(py::init<>())
        .def(py::init<::smoke::StructConstants::SomeStruct>(), py::arg("struct_field"))
        ;
}

