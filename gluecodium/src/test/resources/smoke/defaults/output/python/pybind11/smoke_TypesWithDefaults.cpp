

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
#include "gluecodium/Optional.h"
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/TypesWithDefaults.h"
#include "cstdint"
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
        .def_property("int_field", [](const StructWithDefaults& self) -> decltype(auto) {
            return
                (self.int_field)
            ;
        }, [](StructWithDefaults& self, const int32_t value) {

                self.int_field = value;

        })
        .def_property("uint_field", [](const StructWithDefaults& self) -> decltype(auto) {
            return
                (self.uint_field)
            ;
        }, [](StructWithDefaults& self, const uint32_t value) {

                self.uint_field = value;

        })
        .def_property("float_field", [](const StructWithDefaults& self) -> decltype(auto) {
            return
                (self.float_field)
            ;
        }, [](StructWithDefaults& self, const float value) {

                self.float_field = value;

        })
        .def_property("double_field", [](const StructWithDefaults& self) -> decltype(auto) {
            return
                (self.double_field)
            ;
        }, [](StructWithDefaults& self, const double value) {

                self.double_field = value;

        })
        .def_property("bool_field", [](const StructWithDefaults& self) -> decltype(auto) {
            return
                (self.bool_field)
            ;
        }, [](StructWithDefaults& self, const bool value) {

                self.bool_field = value;

        })
        .def_property("string_field", [](const StructWithDefaults& self) -> decltype(auto) {
            return
                (self.string_field)
            ;
        }, [](StructWithDefaults& self, const ::std::string& value) {

                self.string_field = value;

        })
        .def(py::init<>())
        .def(py::init<int32_t, uint32_t, float, double, bool, ::std::string>(), py::arg("int_field"), py::arg("uint_field"), py::arg("float_field"), py::arg("double_field"), py::arg("bool_field"), py::arg("string_field"))
        ;

auto cls_TypesWithDefaultsImmutableStructWithDefaults = py::class_<ImmutableStructWithDefaults>(cls_TypesWithDefaults, "ImmutableStructWithDefaults")
        .def_property_readonly("int_field", [](const ImmutableStructWithDefaults& self) -> decltype(auto) {
            return
                (self.int_field)
            ;
        })
        .def_property_readonly("uint_field", [](const ImmutableStructWithDefaults& self) -> decltype(auto) {
            return
                (self.uint_field)
            ;
        })
        .def_property_readonly("float_field", [](const ImmutableStructWithDefaults& self) -> decltype(auto) {
            return
                (self.float_field)
            ;
        })
        .def_property_readonly("double_field", [](const ImmutableStructWithDefaults& self) -> decltype(auto) {
            return
                (self.double_field)
            ;
        })
        .def_property_readonly("bool_field", [](const ImmutableStructWithDefaults& self) -> decltype(auto) {
            return
                (self.bool_field)
            ;
        })
        .def_property_readonly("string_field", [](const ImmutableStructWithDefaults& self) -> decltype(auto) {
            return
                (self.string_field)
            ;
        })
        .def(py::init<uint32_t, bool>(), py::arg("uint_field"), py::arg("bool_field"))
        .def(py::init<int32_t, uint32_t, float, double, bool, ::std::string>(), py::arg("int_field"), py::arg("uint_field"), py::arg("float_field"), py::arg("double_field"), py::arg("bool_field"), py::arg("string_field"))
        ;

auto cls_TypesWithDefaultsImmutableStructWithCollections = py::class_<ImmutableStructWithCollections>(cls_TypesWithDefaults, "ImmutableStructWithCollections")
        .def_property_readonly("nullable_list_field", [](const ImmutableStructWithCollections& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.nullable_list_field)
            );
        })
        .def_property_readonly("empty_list_field", [](const ImmutableStructWithCollections& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.empty_list_field)
            );
        })
        .def_property_readonly("values_list_field", [](const ImmutableStructWithCollections& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.values_list_field)
            );
        })
        .def_property_readonly("nullable_map_field", [](const ImmutableStructWithCollections& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.nullable_map_field)
            );
        })
        .def_property_readonly("empty_map_field", [](const ImmutableStructWithCollections& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.empty_map_field)
            );
        })
        .def_property_readonly("values_map_field", [](const ImmutableStructWithCollections& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.values_map_field)
            );
        })
        .def_property_readonly("nullable_set_field", [](const ImmutableStructWithCollections& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.nullable_set_field)
            );
        })
        .def_property_readonly("empty_set_field", [](const ImmutableStructWithCollections& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.empty_set_field)
            );
        })
        .def_property_readonly("values_set_field", [](const ImmutableStructWithCollections& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.values_set_field)
            );
        })
        .def(py::init<>())
        .def(py::init<::gluecodium::optional< ::std::vector< int32_t > >, ::std::vector< int32_t >, ::std::vector< int32_t >, ::gluecodium::optional< ::std::unordered_map< int32_t, ::std::string > >, ::std::unordered_map< int32_t, ::std::string >, ::std::unordered_map< int32_t, ::std::string >, ::gluecodium::optional< ::std::unordered_set< ::std::string > >, ::std::unordered_set< ::std::string >, ::std::unordered_set< ::std::string >>(), py::arg("nullable_list_field"), py::arg("empty_list_field"), py::arg("values_list_field"), py::arg("nullable_map_field"), py::arg("empty_map_field"), py::arg("values_map_field"), py::arg("nullable_set_field"), py::arg("empty_set_field"), py::arg("values_set_field"))
        ;

auto cls_TypesWithDefaultsImmutableStructWithFieldConstructorAndCollections = py::class_<ImmutableStructWithFieldConstructorAndCollections>(cls_TypesWithDefaults, "ImmutableStructWithFieldConstructorAndCollections")
        .def_property_readonly("nullable_list_field", [](const ImmutableStructWithFieldConstructorAndCollections& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.nullable_list_field)
            );
        })
        .def_property_readonly("empty_list_field", [](const ImmutableStructWithFieldConstructorAndCollections& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.empty_list_field)
            );
        })
        .def_property_readonly("values_list_field", [](const ImmutableStructWithFieldConstructorAndCollections& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.values_list_field)
            );
        })
        .def_property_readonly("nullable_map_field", [](const ImmutableStructWithFieldConstructorAndCollections& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.nullable_map_field)
            );
        })
        .def_property_readonly("empty_map_field", [](const ImmutableStructWithFieldConstructorAndCollections& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.empty_map_field)
            );
        })
        .def_property_readonly("values_map_field", [](const ImmutableStructWithFieldConstructorAndCollections& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.values_map_field)
            );
        })
        .def_property_readonly("nullable_set_field", [](const ImmutableStructWithFieldConstructorAndCollections& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.nullable_set_field)
            );
        })
        .def_property_readonly("empty_set_field", [](const ImmutableStructWithFieldConstructorAndCollections& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.empty_set_field)
            );
        })
        .def_property_readonly("values_set_field", [](const ImmutableStructWithFieldConstructorAndCollections& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.values_set_field)
            );
        })
        .def_property_readonly("some_field", [](const ImmutableStructWithFieldConstructorAndCollections& self) -> decltype(auto) {
            return
                (self.some_field)
            ;
        })
        .def_property_readonly("another_field", [](const ImmutableStructWithFieldConstructorAndCollections& self) -> decltype(auto) {
            return
                (self.another_field)
            ;
        })
        .def(py::init<>())
        .def(py::init<::gluecodium::optional< ::std::vector< int32_t > >, ::std::vector< int32_t >, ::std::vector< int32_t >, ::gluecodium::optional< ::std::unordered_map< int32_t, ::std::string > >, ::std::unordered_map< int32_t, ::std::string >, ::std::unordered_map< int32_t, ::std::string >, ::gluecodium::optional< ::std::unordered_set< ::std::string > >, ::std::unordered_set< ::std::string >, ::std::unordered_set< ::std::string >, int32_t, int32_t>(), py::arg("nullable_list_field"), py::arg("empty_list_field"), py::arg("values_list_field"), py::arg("nullable_map_field"), py::arg("empty_map_field"), py::arg("values_map_field"), py::arg("nullable_set_field"), py::arg("empty_set_field"), py::arg("values_set_field"), py::arg("some_field"), py::arg("another_field"))
        .def(py::init<int32_t, int32_t>(), py::arg("some_field"), py::arg("another_field"))
        ;

auto cls_TypesWithDefaultsSomeImmutableStructWithDefaults = py::class_<SomeImmutableStructWithDefaults>(cls_TypesWithDefaults, "SomeImmutableStructWithDefaults")
        .def_property_readonly("int_field", [](const SomeImmutableStructWithDefaults& self) -> decltype(auto) {
            return
                (self.int_field)
            ;
        })
        .def(py::init<>())
        .def(py::init<int32_t>(), py::arg("int_field"))
        ;

auto cls_TypesWithDefaultsImmutableStructWithFieldUsingImmutableStruct = py::class_<ImmutableStructWithFieldUsingImmutableStruct>(cls_TypesWithDefaults, "ImmutableStructWithFieldUsingImmutableStruct")
        .def_property_readonly("some_field1", [](const ImmutableStructWithFieldUsingImmutableStruct& self) -> decltype(auto) {
            return
                (self.some_field1)
            ;
        })
        .def_property_readonly("some_field2", [](const ImmutableStructWithFieldUsingImmutableStruct& self) -> decltype(auto) {
            return
                (self.some_field2)
            ;
        })
        .def(py::init<>())
        .def(py::init<::smoke::TypesWithDefaults::SomeImmutableStructWithDefaults, ::smoke::TypesWithDefaults::ImmutableStructWithCollections>(), py::arg("some_field1"), py::arg("some_field2"))
        ;

auto cls_TypesWithDefaultsImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct = py::class_<ImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct>(cls_TypesWithDefaults, "ImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct")
        .def_property_readonly("some_field1", [](const ImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct& self) -> decltype(auto) {
            return
                (self.some_field1)
            ;
        })
        .def_property_readonly("some_field2", [](const ImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct& self) -> decltype(auto) {
            return
                (self.some_field2)
            ;
        })
        .def_property_readonly("some_field", [](const ImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct& self) -> decltype(auto) {
            return
                (self.some_field)
            ;
        })
        .def_property_readonly("another_field", [](const ImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct& self) -> decltype(auto) {
            return
                (self.another_field)
            ;
        })
        .def(py::init<>())
        .def(py::init<::smoke::TypesWithDefaults::SomeImmutableStructWithDefaults, ::smoke::TypesWithDefaults::ImmutableStructWithCollections, int32_t, int32_t>(), py::arg("some_field1"), py::arg("some_field2"), py::arg("some_field"), py::arg("another_field"))
        .def(py::init<int32_t, int32_t>(), py::arg("some_field"), py::arg("another_field"))
        ;

auto cls_TypesWithDefaultsImmutableStructWithNullableFieldUsingImmutableStruct = py::class_<ImmutableStructWithNullableFieldUsingImmutableStruct>(cls_TypesWithDefaults, "ImmutableStructWithNullableFieldUsingImmutableStruct")
        .def_property_readonly("some_field1", [](const ImmutableStructWithNullableFieldUsingImmutableStruct& self) -> decltype(auto) {
            return
                (self.some_field1)
            ;
        })
        .def_property_readonly("some_field2", [](const ImmutableStructWithNullableFieldUsingImmutableStruct& self) -> decltype(auto) {
            return
                (self.some_field2)
            ;
        })
        .def(py::init<>())
        .def(py::init<::gluecodium::optional< ::smoke::TypesWithDefaults::SomeImmutableStructWithDefaults >, ::gluecodium::optional< ::smoke::TypesWithDefaults::ImmutableStructWithCollections >>(), py::arg("some_field1"), py::arg("some_field2"))
        ;

auto cls_TypesWithDefaultsImmutableStructWithFieldConstructorAndNullableFieldUsingImmutableStruct = py::class_<ImmutableStructWithFieldConstructorAndNullableFieldUsingImmutableStruct>(cls_TypesWithDefaults, "ImmutableStructWithFieldConstructorAndNullableFieldUsingImmutableStruct")
        .def_property_readonly("some_field1", [](const ImmutableStructWithFieldConstructorAndNullableFieldUsingImmutableStruct& self) -> decltype(auto) {
            return
                (self.some_field1)
            ;
        })
        .def_property_readonly("some_field2", [](const ImmutableStructWithFieldConstructorAndNullableFieldUsingImmutableStruct& self) -> decltype(auto) {
            return
                (self.some_field2)
            ;
        })
        .def_property_readonly("some_field", [](const ImmutableStructWithFieldConstructorAndNullableFieldUsingImmutableStruct& self) -> decltype(auto) {
            return
                (self.some_field)
            ;
        })
        .def_property_readonly("another_field", [](const ImmutableStructWithFieldConstructorAndNullableFieldUsingImmutableStruct& self) -> decltype(auto) {
            return
                (self.another_field)
            ;
        })
        .def(py::init<>())
        .def(py::init<::gluecodium::optional< ::smoke::TypesWithDefaults::SomeImmutableStructWithDefaults >, ::gluecodium::optional< ::smoke::TypesWithDefaults::ImmutableStructWithCollections >, int32_t, int32_t>(), py::arg("some_field1"), py::arg("some_field2"), py::arg("some_field"), py::arg("another_field"))
        .def(py::init<int32_t, int32_t>(), py::arg("some_field"), py::arg("another_field"))
        ;


}
