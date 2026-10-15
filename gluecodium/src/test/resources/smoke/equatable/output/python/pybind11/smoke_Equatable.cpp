

#include <Python.h>
#include <pybind11/pybind11.h>
#include "_opaque_types.h"
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
#include "gluecodium/VectorHash.h"
#include "smoke/Equatable.h"
#include "cstdint"
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
        .def_property("bool_field", [](const EquatableStruct& self) -> decltype(auto) {
            return
                (self.bool_field)
            ;
        }, [](EquatableStruct& self, const bool value) {

                self.bool_field = value;

        })
        .def_property("int_field", [](const EquatableStruct& self) -> decltype(auto) {
            return
                (self.int_field)
            ;
        }, [](EquatableStruct& self, const int32_t value) {

                self.int_field = value;

        })
        .def_property("long_field", [](const EquatableStruct& self) -> decltype(auto) {
            return
                (self.long_field)
            ;
        }, [](EquatableStruct& self, const int64_t value) {

                self.long_field = value;

        })
        .def_property("float_field", [](const EquatableStruct& self) -> decltype(auto) {
            return
                (self.float_field)
            ;
        }, [](EquatableStruct& self, const float value) {

                self.float_field = value;

        })
        .def_property("double_field", [](const EquatableStruct& self) -> decltype(auto) {
            return
                (self.double_field)
            ;
        }, [](EquatableStruct& self, const double value) {

                self.double_field = value;

        })
        .def_property("string_field", [](const EquatableStruct& self) -> decltype(auto) {
            return
                (self.string_field)
            ;
        }, [](EquatableStruct& self, const ::std::string& value) {

                self.string_field = value;

        })
        .def_property("struct_field", [](const EquatableStruct& self) -> decltype(auto) {
            return
                (self.struct_field)
            ;
        }, [](EquatableStruct& self, const ::smoke::Equatable::NestedEquatableStruct& value) {

                self.struct_field = value;

        })
        .def_property("enum_field", [](const EquatableStruct& self) -> decltype(auto) {
            return
                (self.enum_field)
            ;
        }, [](EquatableStruct& self, const ::smoke::Equatable::SomeEnum value) {

                self.enum_field = value;

        })
        .def_property("array_field", [](const EquatableStruct& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.array_field)
            );
        }, [](EquatableStruct& self, const ::std::vector< ::std::string >& value) {

                self.array_field = value;

        })
        .def_property("map_field", [](const EquatableStruct& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.map_field)
            );
        }, [](EquatableStruct& self, const ::std::unordered_map< int32_t, ::std::string >& value) {

                self.map_field = value;

        })
        .def(py::init<>())
        .def(py::init<bool, int32_t, int64_t, float, double, ::std::string, ::smoke::Equatable::NestedEquatableStruct, ::smoke::Equatable::SomeEnum, ::std::vector< ::std::string >, ::std::unordered_map< int32_t, ::std::string >>(), py::arg("bool_field"), py::arg("int_field"), py::arg("long_field"), py::arg("float_field"), py::arg("double_field"), py::arg("string_field"), py::arg("struct_field"), py::arg("enum_field"), py::arg("array_field"), py::arg("map_field"))
        .def("__gluecodium_copy__", [](const EquatableStruct& self) { return EquatableStruct(self); })
        .def("__gluecodium_equals__", [](const EquatableStruct& lhs, const EquatableStruct& rhs) { return lhs == rhs; })
        .def("__gluecodium_hash__", [](const EquatableStruct& self) { return gluecodium::hash<EquatableStruct>{}(self); })
        ;

auto cls_EquatableEquatableNullableStruct = py::class_<EquatableNullableStruct>(cls_Equatable, "EquatableNullableStruct")
        .def_property("bool_field", [](const EquatableNullableStruct& self) -> decltype(auto) {
            return
                (self.bool_field)
            ;
        }, [](EquatableNullableStruct& self, const ::gluecodium::optional< bool >& value) {

                self.bool_field = value;

        })
        .def_property("int_field", [](const EquatableNullableStruct& self) -> decltype(auto) {
            return
                (self.int_field)
            ;
        }, [](EquatableNullableStruct& self, const ::gluecodium::optional< int32_t >& value) {

                self.int_field = value;

        })
        .def_property("uint_field", [](const EquatableNullableStruct& self) -> decltype(auto) {
            return
                (self.uint_field)
            ;
        }, [](EquatableNullableStruct& self, const ::gluecodium::optional< uint16_t >& value) {

                self.uint_field = value;

        })
        .def_property("float_field", [](const EquatableNullableStruct& self) -> decltype(auto) {
            return
                (self.float_field)
            ;
        }, [](EquatableNullableStruct& self, const ::gluecodium::optional< float >& value) {

                self.float_field = value;

        })
        .def_property("string_field", [](const EquatableNullableStruct& self) -> decltype(auto) {
            return
                (self.string_field)
            ;
        }, [](EquatableNullableStruct& self, const ::gluecodium::optional< ::std::string >& value) {

                self.string_field = value;

        })
        .def_property("struct_field", [](const EquatableNullableStruct& self) -> decltype(auto) {
            return
                (self.struct_field)
            ;
        }, [](EquatableNullableStruct& self, const ::gluecodium::optional< ::smoke::Equatable::NestedEquatableStruct >& value) {

                self.struct_field = value;

        })
        .def_property("enum_field", [](const EquatableNullableStruct& self) -> decltype(auto) {
            return
                (self.enum_field)
            ;
        }, [](EquatableNullableStruct& self, const ::gluecodium::optional< ::smoke::Equatable::SomeEnum >& value) {

                self.enum_field = value;

        })
        .def_property("array_field", [](const EquatableNullableStruct& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.array_field)
            );
        }, [](EquatableNullableStruct& self, const ::gluecodium::optional< ::std::vector< ::std::string > >& value) {

                self.array_field = value;

        })
        .def_property("map_field", [](const EquatableNullableStruct& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.map_field)
            );
        }, [](EquatableNullableStruct& self, const ::gluecodium::optional< ::std::unordered_map< int32_t, ::std::string > >& value) {

                self.map_field = value;

        })
        .def(py::init<>())
        .def(py::init<::gluecodium::optional< bool >, ::gluecodium::optional< int32_t >, ::gluecodium::optional< uint16_t >, ::gluecodium::optional< float >, ::gluecodium::optional< ::std::string >, ::gluecodium::optional< ::smoke::Equatable::NestedEquatableStruct >, ::gluecodium::optional< ::smoke::Equatable::SomeEnum >, ::gluecodium::optional< ::std::vector< ::std::string > >, ::gluecodium::optional< ::std::unordered_map< int32_t, ::std::string > >>(), py::arg("bool_field"), py::arg("int_field"), py::arg("uint_field"), py::arg("float_field"), py::arg("string_field"), py::arg("struct_field"), py::arg("enum_field"), py::arg("array_field"), py::arg("map_field"))
        .def("__gluecodium_copy__", [](const EquatableNullableStruct& self) { return EquatableNullableStruct(self); })
        .def("__gluecodium_equals__", [](const EquatableNullableStruct& lhs, const EquatableNullableStruct& rhs) { return lhs == rhs; })
        .def("__gluecodium_hash__", [](const EquatableNullableStruct& self) { return gluecodium::hash<EquatableNullableStruct>{}(self); })
        ;

auto cls_EquatableNestedEquatableStruct = py::class_<NestedEquatableStruct>(cls_Equatable, "NestedEquatableStruct")
        .def_property("foo_field", [](const NestedEquatableStruct& self) -> decltype(auto) {
            return
                (self.foo_field)
            ;
        }, [](NestedEquatableStruct& self, const ::std::string& value) {

                self.foo_field = value;

        })
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("foo_field"))
        .def("__gluecodium_copy__", [](const NestedEquatableStruct& self) { return NestedEquatableStruct(self); })
        .def("__gluecodium_equals__", [](const NestedEquatableStruct& lhs, const NestedEquatableStruct& rhs) { return lhs == rhs; })
        .def("__gluecodium_hash__", [](const NestedEquatableStruct& self) { return gluecodium::hash<NestedEquatableStruct>{}(self); })
        ;

auto cls_EquatableSomeEnum = py::enum_<SomeEnum>(cls_Equatable, "SomeEnum")
        .value("FOO", SomeEnum::FOO)
        .value("BAR", SomeEnum::BAR)
        ;


}
