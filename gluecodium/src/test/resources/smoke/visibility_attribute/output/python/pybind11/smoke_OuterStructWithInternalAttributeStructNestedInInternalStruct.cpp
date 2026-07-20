

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/OuterStructWithInternalAttribute.h"
#include "cstdint"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using StructNestedInInternalStruct = ::smoke::OuterStructWithInternalAttribute::StructNestedInInternalStruct;

void register_OuterStructWithInternalAttributeStructNestedInInternalStruct(py::module_& module) {
    py::class_<StructNestedInInternalStruct>(module, "OuterStructWithInternalAttributeStructNestedInInternalStruct")
        .def_readwrite("some_field", &StructNestedInInternalStruct::some_field)
        .def(py::init<>())
        ;
}

