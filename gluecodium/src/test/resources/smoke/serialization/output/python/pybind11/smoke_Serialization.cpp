

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
        .def_readwrite("bool_field", &SerializableStruct::bool_field)
        .def_readwrite("byte_field", &SerializableStruct::byte_field)
        .def_readwrite("short_field", &SerializableStruct::short_field)
        .def_readwrite("int_field", &SerializableStruct::int_field)
        .def_readwrite("long_field", &SerializableStruct::long_field)
        .def_readwrite("float_field", &SerializableStruct::float_field)
        .def_readwrite("double_field", &SerializableStruct::double_field)
        .def_readwrite("string_field", &SerializableStruct::string_field)
        .def_readwrite("struct_field", &SerializableStruct::struct_field)
        .def_readwrite("byte_buffer_field", &SerializableStruct::byte_buffer_field)
        .def_readwrite("array_field", &SerializableStruct::array_field)
        .def_readwrite("struct_array_field", &SerializableStruct::struct_array_field)
        .def_readwrite("map_field", &SerializableStruct::map_field)
        .def_readwrite("set_field", &SerializableStruct::set_field)
        .def_readwrite("enum_set_field", &SerializableStruct::enum_set_field)
        .def_readwrite("enum_field", &SerializableStruct::enum_field)
        .def(py::init<>())
        .def(py::init<bool, int8_t, int16_t, int32_t, uint32_t, float, double, ::std::string, ::smoke::Serialization::NestedSerializableStruct, ::std::shared_ptr< ::std::vector< uint8_t > >, ::std::vector< ::std::string >, ::std::vector< ::smoke::Serialization::NestedSerializableStruct >, ::std::unordered_map< int32_t, ::std::string >, ::std::unordered_set< ::std::string >, ::std::unordered_set< ::smoke::Serialization::SomeEnum, ::gluecodium::hash< ::smoke::Serialization::SomeEnum > >, ::smoke::Serialization::SomeEnum>(), py::arg("bool_field"), py::arg("byte_field"), py::arg("short_field"), py::arg("int_field"), py::arg("long_field"), py::arg("float_field"), py::arg("double_field"), py::arg("string_field"), py::arg("struct_field"), py::arg("byte_buffer_field"), py::arg("array_field"), py::arg("struct_array_field"), py::arg("map_field"), py::arg("set_field"), py::arg("enum_set_field"), py::arg("enum_field"))
        ;

auto cls_SerializationNestedSerializableStruct = py::class_<NestedSerializableStruct>(cls_Serialization, "NestedSerializableStruct")
        .def_readwrite("some_field", &NestedSerializableStruct::some_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("some_field"))
        ;

auto cls_SerializationSomeEnum = py::enum_<SomeEnum>(cls_Serialization, "SomeEnum")
        .value("FOO", SomeEnum::FOO)
        .value("BAR", SomeEnum::BAR)
        ;


}
