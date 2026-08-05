

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
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/TypesWithDefaults.h"
#include "cstdint"
#include "optional"
#include "string"
#include "unordered_map"
#include "unordered_set"
#include "vector"

using TypesWithDefaults = ::smoke::TypesWithDefaults;
using StructWithDefaults = ::smoke::TypesWithDefaults::StructWithDefaults;
using ImmutableStructWithDefaults = ::smoke::TypesWithDefaults::ImmutableStructWithDefaults;
using ImmutableStructWithCollections = ::smoke::TypesWithDefaults::ImmutableStructWithCollections;
using ImmutableStructWithFieldConstructorAndCollections = ::smoke::TypesWithDefaults::ImmutableStructWithFieldConstructorAndCollections;
using SomeImmutableStructWithDefaults = ::smoke::TypesWithDefaults::SomeImmutableStructWithDefaults;
using ImmutableStructWithFieldUsingImmutableStruct = ::smoke::TypesWithDefaults::ImmutableStructWithFieldUsingImmutableStruct;
using ImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct = ::smoke::TypesWithDefaults::ImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct;
using ImmutableStructWithNullableFieldUsingImmutableStruct = ::smoke::TypesWithDefaults::ImmutableStructWithNullableFieldUsingImmutableStruct;
using ImmutableStructWithFieldConstructorAndNullableFieldUsingImmutableStruct = ::smoke::TypesWithDefaults::ImmutableStructWithFieldConstructorAndNullableFieldUsingImmutableStruct;



void register_smoke_TypesWithDefaults(py::module_& module) {
auto cls_TypesWithDefaults = py::class_<TypesWithDefaults>(module, "smoke_TypesWithDefaults")
        .def(py::init<>())
        ;

auto cls_TypesWithDefaultsStructWithDefaults = py::class_<StructWithDefaults>(cls_TypesWithDefaults, "StructWithDefaults")
        .def_readwrite("int_field", &StructWithDefaults::int_field)
        .def_readwrite("uint_field", &StructWithDefaults::uint_field)
        .def_readwrite("float_field", &StructWithDefaults::float_field)
        .def_readwrite("double_field", &StructWithDefaults::double_field)
        .def_readwrite("bool_field", &StructWithDefaults::bool_field)
        .def_readwrite("string_field", &StructWithDefaults::string_field)
        .def(py::init<>())
        .def(py::init<int32_t, uint32_t, float, double, bool, ::std::string>(), py::arg("int_field"), py::arg("uint_field"), py::arg("float_field"), py::arg("double_field"), py::arg("bool_field"), py::arg("string_field"))
        ;

auto cls_TypesWithDefaultsImmutableStructWithDefaults = py::class_<ImmutableStructWithDefaults>(cls_TypesWithDefaults, "ImmutableStructWithDefaults")
        .def_readonly("int_field", &ImmutableStructWithDefaults::int_field)
        .def_readonly("uint_field", &ImmutableStructWithDefaults::uint_field)
        .def_readonly("float_field", &ImmutableStructWithDefaults::float_field)
        .def_readonly("double_field", &ImmutableStructWithDefaults::double_field)
        .def_readonly("bool_field", &ImmutableStructWithDefaults::bool_field)
        .def_readonly("string_field", &ImmutableStructWithDefaults::string_field)
        .def(py::init<uint32_t, bool>(), py::arg("uint_field"), py::arg("bool_field"))
        .def(py::init<int32_t, uint32_t, float, double, bool, ::std::string>(), py::arg("int_field"), py::arg("uint_field"), py::arg("float_field"), py::arg("double_field"), py::arg("bool_field"), py::arg("string_field"))
        ;

auto cls_TypesWithDefaultsImmutableStructWithCollections = py::class_<ImmutableStructWithCollections>(cls_TypesWithDefaults, "ImmutableStructWithCollections")
        .def_readonly("nullable_list_field", &ImmutableStructWithCollections::nullable_list_field)
        .def_readonly("empty_list_field", &ImmutableStructWithCollections::empty_list_field)
        .def_readonly("values_list_field", &ImmutableStructWithCollections::values_list_field)
        .def_readonly("nullable_map_field", &ImmutableStructWithCollections::nullable_map_field)
        .def_readonly("empty_map_field", &ImmutableStructWithCollections::empty_map_field)
        .def_readonly("values_map_field", &ImmutableStructWithCollections::values_map_field)
        .def_readonly("nullable_set_field", &ImmutableStructWithCollections::nullable_set_field)
        .def_readonly("empty_set_field", &ImmutableStructWithCollections::empty_set_field)
        .def_readonly("values_set_field", &ImmutableStructWithCollections::values_set_field)
        .def(py::init<>())
        .def(py::init<std::optional< ::std::vector< int32_t > >, ::std::vector< int32_t >, ::std::vector< int32_t >, std::optional< ::std::unordered_map< int32_t, ::std::string > >, ::std::unordered_map< int32_t, ::std::string >, ::std::unordered_map< int32_t, ::std::string >, std::optional< ::std::unordered_set< ::std::string > >, ::std::unordered_set< ::std::string >, ::std::unordered_set< ::std::string >>(), py::arg("nullable_list_field"), py::arg("empty_list_field"), py::arg("values_list_field"), py::arg("nullable_map_field"), py::arg("empty_map_field"), py::arg("values_map_field"), py::arg("nullable_set_field"), py::arg("empty_set_field"), py::arg("values_set_field"))
        ;

auto cls_TypesWithDefaultsImmutableStructWithFieldConstructorAndCollections = py::class_<ImmutableStructWithFieldConstructorAndCollections>(cls_TypesWithDefaults, "ImmutableStructWithFieldConstructorAndCollections")
        .def_readonly("nullable_list_field", &ImmutableStructWithFieldConstructorAndCollections::nullable_list_field)
        .def_readonly("empty_list_field", &ImmutableStructWithFieldConstructorAndCollections::empty_list_field)
        .def_readonly("values_list_field", &ImmutableStructWithFieldConstructorAndCollections::values_list_field)
        .def_readonly("nullable_map_field", &ImmutableStructWithFieldConstructorAndCollections::nullable_map_field)
        .def_readonly("empty_map_field", &ImmutableStructWithFieldConstructorAndCollections::empty_map_field)
        .def_readonly("values_map_field", &ImmutableStructWithFieldConstructorAndCollections::values_map_field)
        .def_readonly("nullable_set_field", &ImmutableStructWithFieldConstructorAndCollections::nullable_set_field)
        .def_readonly("empty_set_field", &ImmutableStructWithFieldConstructorAndCollections::empty_set_field)
        .def_readonly("values_set_field", &ImmutableStructWithFieldConstructorAndCollections::values_set_field)
        .def_readonly("some_field", &ImmutableStructWithFieldConstructorAndCollections::some_field)
        .def_readonly("another_field", &ImmutableStructWithFieldConstructorAndCollections::another_field)
        .def(py::init<>())
        .def(py::init<std::optional< ::std::vector< int32_t > >, ::std::vector< int32_t >, ::std::vector< int32_t >, std::optional< ::std::unordered_map< int32_t, ::std::string > >, ::std::unordered_map< int32_t, ::std::string >, ::std::unordered_map< int32_t, ::std::string >, std::optional< ::std::unordered_set< ::std::string > >, ::std::unordered_set< ::std::string >, ::std::unordered_set< ::std::string >, int32_t, int32_t>(), py::arg("nullable_list_field"), py::arg("empty_list_field"), py::arg("values_list_field"), py::arg("nullable_map_field"), py::arg("empty_map_field"), py::arg("values_map_field"), py::arg("nullable_set_field"), py::arg("empty_set_field"), py::arg("values_set_field"), py::arg("some_field"), py::arg("another_field"))
        .def(py::init<int32_t, int32_t>(), py::arg("some_field"), py::arg("another_field"))
        ;

auto cls_TypesWithDefaultsSomeImmutableStructWithDefaults = py::class_<SomeImmutableStructWithDefaults>(cls_TypesWithDefaults, "SomeImmutableStructWithDefaults")
        .def_readonly("int_field", &SomeImmutableStructWithDefaults::int_field)
        .def(py::init<>())
        .def(py::init<int32_t>(), py::arg("int_field"))
        ;

auto cls_TypesWithDefaultsImmutableStructWithFieldUsingImmutableStruct = py::class_<ImmutableStructWithFieldUsingImmutableStruct>(cls_TypesWithDefaults, "ImmutableStructWithFieldUsingImmutableStruct")
        .def_readonly("some_field1", &ImmutableStructWithFieldUsingImmutableStruct::some_field1)
        .def_readonly("some_field2", &ImmutableStructWithFieldUsingImmutableStruct::some_field2)
        .def(py::init<>())
        .def(py::init<::smoke::TypesWithDefaults::SomeImmutableStructWithDefaults, ::smoke::TypesWithDefaults::ImmutableStructWithCollections>(), py::arg("some_field1"), py::arg("some_field2"))
        ;

auto cls_TypesWithDefaultsImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct = py::class_<ImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct>(cls_TypesWithDefaults, "ImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct")
        .def_readonly("some_field1", &ImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct::some_field1)
        .def_readonly("some_field2", &ImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct::some_field2)
        .def_readonly("some_field", &ImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct::some_field)
        .def_readonly("another_field", &ImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct::another_field)
        .def(py::init<>())
        .def(py::init<::smoke::TypesWithDefaults::SomeImmutableStructWithDefaults, ::smoke::TypesWithDefaults::ImmutableStructWithCollections, int32_t, int32_t>(), py::arg("some_field1"), py::arg("some_field2"), py::arg("some_field"), py::arg("another_field"))
        .def(py::init<int32_t, int32_t>(), py::arg("some_field"), py::arg("another_field"))
        ;

auto cls_TypesWithDefaultsImmutableStructWithNullableFieldUsingImmutableStruct = py::class_<ImmutableStructWithNullableFieldUsingImmutableStruct>(cls_TypesWithDefaults, "ImmutableStructWithNullableFieldUsingImmutableStruct")
        .def_readonly("some_field1", &ImmutableStructWithNullableFieldUsingImmutableStruct::some_field1)
        .def_readonly("some_field2", &ImmutableStructWithNullableFieldUsingImmutableStruct::some_field2)
        .def(py::init<>())
        .def(py::init<std::optional< ::smoke::TypesWithDefaults::SomeImmutableStructWithDefaults >, std::optional< ::smoke::TypesWithDefaults::ImmutableStructWithCollections >>(), py::arg("some_field1"), py::arg("some_field2"))
        ;

auto cls_TypesWithDefaultsImmutableStructWithFieldConstructorAndNullableFieldUsingImmutableStruct = py::class_<ImmutableStructWithFieldConstructorAndNullableFieldUsingImmutableStruct>(cls_TypesWithDefaults, "ImmutableStructWithFieldConstructorAndNullableFieldUsingImmutableStruct")
        .def_readonly("some_field1", &ImmutableStructWithFieldConstructorAndNullableFieldUsingImmutableStruct::some_field1)
        .def_readonly("some_field2", &ImmutableStructWithFieldConstructorAndNullableFieldUsingImmutableStruct::some_field2)
        .def_readonly("some_field", &ImmutableStructWithFieldConstructorAndNullableFieldUsingImmutableStruct::some_field)
        .def_readonly("another_field", &ImmutableStructWithFieldConstructorAndNullableFieldUsingImmutableStruct::another_field)
        .def(py::init<>())
        .def(py::init<std::optional< ::smoke::TypesWithDefaults::SomeImmutableStructWithDefaults >, std::optional< ::smoke::TypesWithDefaults::ImmutableStructWithCollections >, int32_t, int32_t>(), py::arg("some_field1"), py::arg("some_field2"), py::arg("some_field"), py::arg("another_field"))
        .def(py::init<int32_t, int32_t>(), py::arg("some_field"), py::arg("another_field"))
        ;


}
