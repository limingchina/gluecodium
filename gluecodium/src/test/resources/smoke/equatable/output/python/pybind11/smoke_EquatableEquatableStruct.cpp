

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/Equatable.h"
#include "cstdint"
#include "string"
#include "unordered_map"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using EquatableStruct = ::smoke::Equatable::EquatableStruct;

void register_smoke_EquatableEquatableStruct(py::module_& module) {
    py::class_<EquatableStruct>(module, "EquatableEquatableStruct")
        .def_readwrite("bool_field", &EquatableStruct::bool_field)
        .def_readwrite("int_field", &EquatableStruct::int_field)
        .def_readwrite("long_field", &EquatableStruct::long_field)
        .def_readwrite("float_field", &EquatableStruct::float_field)
        .def_readwrite("double_field", &EquatableStruct::double_field)
        .def_readwrite("string_field", &EquatableStruct::string_field)
        .def_readwrite("struct_field", &EquatableStruct::struct_field)
        .def_readwrite("enum_field", &EquatableStruct::enum_field)
        .def_readwrite("array_field", &EquatableStruct::array_field)
        .def_readwrite("map_field", &EquatableStruct::map_field)
        .def(py::init<>())
        .def(py::init<bool, int32_t, int64_t, float, double, ::std::string, ::smoke::Equatable::NestedEquatableStruct, ::smoke::Equatable::SomeEnum, ::std::vector< ::std::string >, ::std::unordered_map< int32_t, ::std::string >(), py::arg("bool_field"), py::arg("int_field"), py::arg("long_field"), py::arg("float_field"), py::arg("double_field"), py::arg("string_field"), py::arg("struct_field"), py::arg("enum_field"), py::arg("array_field"), py::arg("map_field"))
        ;
}

