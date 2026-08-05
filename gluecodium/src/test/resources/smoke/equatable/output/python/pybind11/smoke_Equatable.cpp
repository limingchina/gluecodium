

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

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

using Equatable = ::smoke::Equatable;
using EquatableStruct = ::smoke::Equatable::EquatableStruct;
using EquatableNullableStruct = ::smoke::Equatable::EquatableNullableStruct;
using NestedEquatableStruct = ::smoke::Equatable::NestedEquatableStruct;
using SomeEnum = ::smoke::Equatable::SomeEnum;



void register_smoke_Equatable(py::module_& module) {
auto cls_Equatable = py::class_<Equatable>(module, "smoke_Equatable")
        .def(py::init<>())
        ;

auto cls_EquatableEquatableStruct = py::class_<EquatableStruct>(cls_Equatable, "EquatableStruct")
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
        .def(py::init<bool, int32_t, int64_t, float, double, ::std::string, ::smoke::Equatable::NestedEquatableStruct, ::smoke::Equatable::SomeEnum, ::std::vector< ::std::string >, ::std::unordered_map< int32_t, ::std::string >>(), py::arg("bool_field"), py::arg("int_field"), py::arg("long_field"), py::arg("float_field"), py::arg("double_field"), py::arg("string_field"), py::arg("struct_field"), py::arg("enum_field"), py::arg("array_field"), py::arg("map_field"))
        .def("__eq__", [](const EquatableStruct& lhs, const EquatableStruct& rhs) { return lhs == rhs; })
        .def("__hash__", [](const EquatableStruct& self) { return gluecodium::hash<EquatableStruct>{}(self); })
        ;

auto cls_EquatableEquatableNullableStruct = py::class_<EquatableNullableStruct>(cls_Equatable, "EquatableNullableStruct")
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
        .def("__eq__", [](const EquatableNullableStruct& lhs, const EquatableNullableStruct& rhs) { return lhs == rhs; })
        .def("__hash__", [](const EquatableNullableStruct& self) { return gluecodium::hash<EquatableNullableStruct>{}(self); })
        ;

auto cls_EquatableNestedEquatableStruct = py::class_<NestedEquatableStruct>(cls_Equatable, "NestedEquatableStruct")
        .def_readwrite("foo_field", &NestedEquatableStruct::foo_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("foo_field"))
        .def("__eq__", [](const NestedEquatableStruct& lhs, const NestedEquatableStruct& rhs) { return lhs == rhs; })
        .def("__hash__", [](const NestedEquatableStruct& self) { return gluecodium::hash<NestedEquatableStruct>{}(self); })
        ;

auto cls_EquatableSomeEnum = py::enum_<SomeEnum>(cls_Equatable, "SomeEnum")
        .value("FOO", SomeEnum::FOO)
        .value("BAR", SomeEnum::BAR)
        ;


}
