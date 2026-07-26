

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
#include "smoke/Structs.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using NestingImmutableStruct = ::smoke::Structs::NestingImmutableStruct;

void register_smoke_StructsNestingImmutableStruct(py::module_& module) {
    py::class_<NestingImmutableStruct>(module, "smoke_StructsNestingImmutableStruct")
        .def_readonly("struct_field", &NestingImmutableStruct::struct_field)
        .def(py::init<::smoke::Structs::AllTypesStruct>(), py::arg("struct_field"))
        ;
}

