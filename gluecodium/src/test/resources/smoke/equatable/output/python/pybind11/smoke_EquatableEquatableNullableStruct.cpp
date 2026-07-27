

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
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/Equatable.h"
#include "cstdint"
#include "optional"
#include "string"
#include "unordered_map"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using EquatableNullableStruct = ::smoke::Equatable::EquatableNullableStruct;

void register_smoke_EquatableEquatableNullableStruct(py::module_& module) {
    py::class_<EquatableNullableStruct>(module, "smoke_EquatableEquatableNullableStruct")
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
        .def(py::init<std::optional< bool >, std::optional< int32_t >, std::optional< uint16_t >, std::optional< float >, std::optional< ::std::string >, std::optional< ::smoke::Equatable::NestedEquatableStruct >, std::optional< ::smoke::Equatable::SomeEnum >, std::optional< ::std::vector< ::std::string > >, std::optional< ::std::unordered_map< int32_t, ::std::string > >>(), py::arg("bool_field"), py::arg("int_field"), py::arg("uint_field"), py::arg("float_field"), py::arg("string_field"), py::arg("struct_field"), py::arg("enum_field"), py::arg("array_field"), py::arg("map_field"))
        .def(py::init<std::optional< bool >, std::optional< int32_t >, std::optional< uint16_t >, std::optional< float >, std::optional< ::std::string >, std::optional< ::smoke::Equatable::NestedEquatableStruct >, std::optional< ::smoke::Equatable::SomeEnum >, std::optional< ::std::vector< ::std::string > >, std::optional< ::std::unordered_map< int32_t, ::std::string > >>(), py::arg("bool_field"), py::arg("int_field"), py::arg("uint_field"), py::arg("float_field"), py::arg("string_field"), py::arg("struct_field"), py::arg("enum_field"), py::arg("array_field"), py::arg("map_field"))
        .def(py::init<std::optional< bool >, std::optional< int32_t >, std::optional< uint16_t >, std::optional< float >, std::optional< ::std::string >, std::optional< ::smoke::Equatable::NestedEquatableStruct >, std::optional< ::smoke::Equatable::SomeEnum >, std::optional< ::std::vector< ::std::string > >, std::optional< ::std::unordered_map< int32_t, ::std::string > >>(), py::arg("bool_field"), py::arg("int_field"), py::arg("uint_field"), py::arg("float_field"), py::arg("string_field"), py::arg("struct_field"), py::arg("enum_field"), py::arg("array_field"), py::arg("map_field"))
        .def(py::init<std::optional< bool >, std::optional< int32_t >, std::optional< uint16_t >, std::optional< float >, std::optional< ::std::string >, std::optional< ::smoke::Equatable::NestedEquatableStruct >, std::optional< ::smoke::Equatable::SomeEnum >, std::optional< ::std::vector< ::std::string > >, std::optional< ::std::unordered_map< int32_t, ::std::string > >>(), py::arg("bool_field"), py::arg("int_field"), py::arg("uint_field"), py::arg("float_field"), py::arg("string_field"), py::arg("struct_field"), py::arg("enum_field"), py::arg("array_field"), py::arg("map_field"))
        .def(py::init<std::optional< bool >, std::optional< int32_t >, std::optional< uint16_t >, std::optional< float >, std::optional< ::std::string >, std::optional< ::smoke::Equatable::NestedEquatableStruct >, std::optional< ::smoke::Equatable::SomeEnum >, std::optional< ::std::vector< ::std::string > >, std::optional< ::std::unordered_map< int32_t, ::std::string > >>(), py::arg("bool_field"), py::arg("int_field"), py::arg("uint_field"), py::arg("float_field"), py::arg("string_field"), py::arg("struct_field"), py::arg("enum_field"), py::arg("array_field"), py::arg("map_field"))
        .def(py::init<std::optional< bool >, std::optional< int32_t >, std::optional< uint16_t >, std::optional< float >, std::optional< ::std::string >, std::optional< ::smoke::Equatable::NestedEquatableStruct >, std::optional< ::smoke::Equatable::SomeEnum >, std::optional< ::std::vector< ::std::string > >, std::optional< ::std::unordered_map< int32_t, ::std::string > >>(), py::arg("bool_field"), py::arg("int_field"), py::arg("uint_field"), py::arg("float_field"), py::arg("string_field"), py::arg("struct_field"), py::arg("enum_field"), py::arg("array_field"), py::arg("map_field"))
        .def(py::init<std::optional< bool >, std::optional< int32_t >, std::optional< uint16_t >, std::optional< float >, std::optional< ::std::string >, std::optional< ::smoke::Equatable::NestedEquatableStruct >, std::optional< ::smoke::Equatable::SomeEnum >, std::optional< ::std::vector< ::std::string > >, std::optional< ::std::unordered_map< int32_t, ::std::string > >>(), py::arg("bool_field"), py::arg("int_field"), py::arg("uint_field"), py::arg("float_field"), py::arg("string_field"), py::arg("struct_field"), py::arg("enum_field"), py::arg("array_field"), py::arg("map_field"))
        .def(py::init<std::optional< bool >, std::optional< int32_t >, std::optional< uint16_t >, std::optional< float >, std::optional< ::std::string >, std::optional< ::smoke::Equatable::NestedEquatableStruct >, std::optional< ::smoke::Equatable::SomeEnum >, std::optional< ::std::vector< ::std::string > >, std::optional< ::std::unordered_map< int32_t, ::std::string > >>(), py::arg("bool_field"), py::arg("int_field"), py::arg("uint_field"), py::arg("float_field"), py::arg("string_field"), py::arg("struct_field"), py::arg("enum_field"), py::arg("array_field"), py::arg("map_field"))
        .def(py::init<std::optional< bool >, std::optional< int32_t >, std::optional< uint16_t >, std::optional< float >, std::optional< ::std::string >, std::optional< ::smoke::Equatable::NestedEquatableStruct >, std::optional< ::smoke::Equatable::SomeEnum >, std::optional< ::std::vector< ::std::string > >, std::optional< ::std::unordered_map< int32_t, ::std::string > >>(), py::arg("bool_field"), py::arg("int_field"), py::arg("uint_field"), py::arg("float_field"), py::arg("string_field"), py::arg("struct_field"), py::arg("enum_field"), py::arg("array_field"), py::arg("map_field"))
        .def("__eq__", [](const EquatableNullableStruct& lhs, const EquatableNullableStruct& rhs) { return lhs == rhs; })
        .def("__hash__", [](const EquatableNullableStruct& self) { return gluecodium::hash<EquatableNullableStruct>{}(self); })
        ;
}

