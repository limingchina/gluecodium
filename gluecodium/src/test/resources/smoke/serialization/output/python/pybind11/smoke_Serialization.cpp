

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
#include "gluecodium/Hash.h"
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/Serialization.h"
#include "cstdint"
#include "memory"
#include "string"
#include "unordered_map"
#include "unordered_set"
#include "vector"

using Serialization = ::smoke::Serialization;
using SerializableStruct = ::smoke::Serialization::SerializableStruct;
using NestedSerializableStruct = ::smoke::Serialization::NestedSerializableStruct;
using SomeEnum = ::smoke::Serialization::SomeEnum;



void register_smoke_Serialization(py::module_& module) {
auto cls_Serialization = py::class_<Serialization>(module, "smoke_Serialization")
        .def(py::init<>())
        ;

auto cls_SerializationSerializableStruct = py::class_<SerializableStruct>(cls_Serialization, "SerializableStruct")
        .def_property("bool_field", [](const SerializableStruct& self) -> decltype(auto) {
            return
                (self.bool_field)
            ;
        }, [](SerializableStruct& self, const bool value) {

                self.bool_field = value;

        })
        .def_property("byte_field", [](const SerializableStruct& self) -> decltype(auto) {
            return
                (self.byte_field)
            ;
        }, [](SerializableStruct& self, const int8_t value) {

                self.byte_field = value;

        })
        .def_property("short_field", [](const SerializableStruct& self) -> decltype(auto) {
            return
                (self.short_field)
            ;
        }, [](SerializableStruct& self, const int16_t value) {

                self.short_field = value;

        })
        .def_property("int_field", [](const SerializableStruct& self) -> decltype(auto) {
            return
                (self.int_field)
            ;
        }, [](SerializableStruct& self, const int32_t value) {

                self.int_field = value;

        })
        .def_property("long_field", [](const SerializableStruct& self) -> decltype(auto) {
            return
                (self.long_field)
            ;
        }, [](SerializableStruct& self, const uint32_t value) {

                self.long_field = value;

        })
        .def_property("float_field", [](const SerializableStruct& self) -> decltype(auto) {
            return
                (self.float_field)
            ;
        }, [](SerializableStruct& self, const float value) {

                self.float_field = value;

        })
        .def_property("double_field", [](const SerializableStruct& self) -> decltype(auto) {
            return
                (self.double_field)
            ;
        }, [](SerializableStruct& self, const double value) {

                self.double_field = value;

        })
        .def_property("string_field", [](const SerializableStruct& self) -> decltype(auto) {
            return
                (self.string_field)
            ;
        }, [](SerializableStruct& self, const ::std::string& value) {

                self.string_field = value;

        })
        .def_property("struct_field", [](const SerializableStruct& self) -> decltype(auto) {
            return
                (self.struct_field)
            ;
        }, [](SerializableStruct& self, const ::smoke::Serialization::NestedSerializableStruct& value) {

                self.struct_field = value;

        })
        .def_property("byte_buffer_field", [](const SerializableStruct& self) -> decltype(auto) {
            return
                (self.byte_buffer_field)
            ;
        }, [](SerializableStruct& self, const ::std::shared_ptr< ::std::vector< uint8_t > >& value) {

                self.byte_buffer_field = value;

        })
        .def_property("array_field", [](const SerializableStruct& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.array_field)
            );
        }, [](SerializableStruct& self, const ::std::vector< ::std::string >& value) {

                self.array_field = value;

        })
        .def_property("struct_array_field", [](const SerializableStruct& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.struct_array_field)
            );
        }, [](SerializableStruct& self, const ::std::vector< ::smoke::Serialization::NestedSerializableStruct >& value) {

                self.struct_array_field = value;

        })
        .def_property("map_field", [](const SerializableStruct& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.map_field)
            );
        }, [](SerializableStruct& self, const ::std::unordered_map< int32_t, ::std::string >& value) {

                self.map_field = value;

        })
        .def_property("set_field", [](const SerializableStruct& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.set_field)
            );
        }, [](SerializableStruct& self, const ::std::unordered_set< ::std::string >& value) {

                self.set_field = value;

        })
        .def_property("enum_set_field", [](const SerializableStruct& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.enum_set_field)
            );
        }, [](SerializableStruct& self, const ::std::unordered_set< ::smoke::Serialization::SomeEnum, ::gluecodium::hash< ::smoke::Serialization::SomeEnum > >& value) {

                self.enum_set_field = value;

        })
        .def_property("enum_field", [](const SerializableStruct& self) -> decltype(auto) {
            return
                (self.enum_field)
            ;
        }, [](SerializableStruct& self, const ::smoke::Serialization::SomeEnum value) {

                self.enum_field = value;

        })
        .def(py::init<>())
        .def(py::init<bool, int8_t, int16_t, int32_t, uint32_t, float, double, ::std::string, ::smoke::Serialization::NestedSerializableStruct, ::std::shared_ptr< ::std::vector< uint8_t > >, ::std::vector< ::std::string >, ::std::vector< ::smoke::Serialization::NestedSerializableStruct >, ::std::unordered_map< int32_t, ::std::string >, ::std::unordered_set< ::std::string >, ::std::unordered_set< ::smoke::Serialization::SomeEnum, ::gluecodium::hash< ::smoke::Serialization::SomeEnum > >, ::smoke::Serialization::SomeEnum>(), py::arg("bool_field"), py::arg("byte_field"), py::arg("short_field"), py::arg("int_field"), py::arg("long_field"), py::arg("float_field"), py::arg("double_field"), py::arg("string_field"), py::arg("struct_field"), py::arg("byte_buffer_field"), py::arg("array_field"), py::arg("struct_array_field"), py::arg("map_field"), py::arg("set_field"), py::arg("enum_set_field"), py::arg("enum_field"))
        ;

auto cls_SerializationNestedSerializableStruct = py::class_<NestedSerializableStruct>(cls_Serialization, "NestedSerializableStruct")
        .def_property("some_field", [](const NestedSerializableStruct& self) -> decltype(auto) {
            return
                (self.some_field)
            ;
        }, [](NestedSerializableStruct& self, const ::std::string& value) {

                self.some_field = value;

        })
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("some_field"))
        ;

auto cls_SerializationSomeEnum = py::enum_<SomeEnum>(cls_Serialization, "SomeEnum")
        .value("FOO", SomeEnum::FOO)
        .value("BAR", SomeEnum::BAR)
        ;


}
