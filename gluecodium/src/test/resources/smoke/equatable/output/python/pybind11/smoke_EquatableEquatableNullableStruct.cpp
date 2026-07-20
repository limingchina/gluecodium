

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/VectorHash.h"
#include "smoke/Equatable.h"
#include "cstdint"
#include "optional"
#include "string"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using EquatableNullableStruct = ::smoke::Equatable::EquatableNullableStruct;

void register_EquatableEquatableNullableStruct(py::module_& module) {
    py::class_<EquatableNullableStruct>(module, "EquatableEquatableNullableStruct")
        .def_readwrite("bool_field", &EquatableNullableStruct::bool_field)
        .def_readwrite("int_field", &EquatableNullableStruct::int_field)
        .def_readwrite("uint_field", &EquatableNullableStruct::uint_field)
        .def_readwrite("float_field", &EquatableNullableStruct::float_field)
        .def_readwrite("string_field", &EquatableNullableStruct::string_field)
        .def_readwrite("struct_field", &EquatableNullableStruct::struct_field)
        .def_readwrite("enum_field", &EquatableNullableStruct::enum_field)
        .def_readwrite("array_field", &EquatableNullableStruct::array_field)
        .def_readwrite("map_field", &EquatableNullableStruct::map_field)
        .def(py::init<>())
        ;
}

