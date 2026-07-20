

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/VectorHash.h"
#include "smoke/Nullable.h"
#include "smoke/SomeInterface.h"
#include "memory"
#include "optional"
#include "string"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using NullableStruct = ::smoke::Nullable::NullableStruct;

void register_NullableNullableStruct(py::module_& module) {
    py::class_<NullableStruct>(module, "NullableNullableStruct")
        .def_readwrite("string_field", &NullableStruct::string_field)
        .def_readwrite("bool_field", &NullableStruct::bool_field)
        .def_readwrite("double_field", &NullableStruct::double_field)
        .def_readwrite("struct_field", &NullableStruct::struct_field)
        .def_readwrite("enum_field", &NullableStruct::enum_field)
        .def_readwrite("array_field", &NullableStruct::array_field)
        .def_readwrite("inline_array_field", &NullableStruct::inline_array_field)
        .def_readwrite("map_field", &NullableStruct::map_field)
        .def_readwrite("instance_field", &NullableStruct::instance_field)
        .def(py::init<>())
        ;
}

