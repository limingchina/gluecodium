

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
using DoubleNestingImmutableStruct = ::smoke::Structs::DoubleNestingImmutableStruct;

void register_smoke_StructsDoubleNestingImmutableStruct(py::module_& module) {
    py::class_<DoubleNestingImmutableStruct>(module, "smoke_StructsDoubleNestingImmutableStruct")
        .def_readonly("nesting_struct_field", &DoubleNestingImmutableStruct::nesting_struct_field)
        .def(py::init<::smoke::Structs::NestingImmutableStruct>(), py::arg("nesting_struct_field"))
        ;
}

