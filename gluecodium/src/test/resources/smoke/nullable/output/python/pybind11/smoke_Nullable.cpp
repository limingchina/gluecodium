

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
#include "smoke/Nullable.h"
#include "smoke/SomeInterface.h"
#include "cstdint"
#include "memory"
#include "optional"
#include "string"
#include "unordered_map"
#include "vector"

using Nullable = ::smoke::Nullable;
using SomeStruct = ::smoke::Nullable::SomeStruct;
using NullableStruct = ::smoke::Nullable::NullableStruct;
using NullableIntsStruct = ::smoke::Nullable::NullableIntsStruct;
using SomeEnum = ::smoke::Nullable::SomeEnum;



void register_smoke_Nullable(py::module_& module) {
auto cls_Nullable = py::class_<Nullable, std::shared_ptr<Nullable>>(module, "smoke_Nullable")
        .def("__gluecodium_id__", [](const Nullable& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("method_with_string", &Nullable::method_with_string, py::arg("input"))
        .def("method_with_boolean", &Nullable::method_with_boolean, py::arg("input"))
        .def("method_with_double", &Nullable::method_with_double, py::arg("input"))
        .def("method_with_int", &Nullable::method_with_int, py::arg("input"))
        .def("method_with_some_struct", &Nullable::method_with_some_struct, py::arg("input"))
        .def("method_with_some_enum", &Nullable::method_with_some_enum, py::arg("input"))
                .def("method_with_some_array", [](Nullable& self, const std::optional< ::std::vector< ::std::string > >& input) -> py::object {
                        return gluecodium::python::to_python_regular(self.method_with_some_array(input));
                }, py::arg("input"))
                .def("method_with_inline_array", [](Nullable& self, const std::optional< ::std::vector< ::std::string > >& input) -> py::object {
                        return gluecodium::python::to_python_regular(self.method_with_inline_array(input));
                }, py::arg("input"))
                .def("method_with_some_map", [](Nullable& self, const std::optional< ::std::unordered_map< int64_t, ::std::string > >& input) -> py::object {
                        return gluecodium::python::to_python_regular(self.method_with_some_map(input));
                }, py::arg("input"))
        .def("method_with_instance", &Nullable::method_with_instance, py::arg("input"))
        .def_property("string_property", py::overload_cast<>(&Nullable::get_string_property, py::const_), py::overload_cast<const std::optional< ::std::string >&>(&Nullable::set_string_property))
        .def_property("is_bool_property", py::overload_cast<>(&Nullable::is_bool_property, py::const_), py::overload_cast<const std::optional< bool >&>(&Nullable::set_bool_property))
        .def_property("double_property", py::overload_cast<>(&Nullable::get_double_property, py::const_), py::overload_cast<const std::optional< double >&>(&Nullable::set_double_property))
        .def_property("int_property", py::overload_cast<>(&Nullable::get_int_property, py::const_), py::overload_cast<const std::optional< int64_t >&>(&Nullable::set_int_property))
        .def_property("struct_property", py::overload_cast<>(&Nullable::get_struct_property, py::const_), py::overload_cast<const std::optional< ::smoke::Nullable::SomeStruct >&>(&Nullable::set_struct_property))
        .def_property("enum_property", py::overload_cast<>(&Nullable::get_enum_property, py::const_), py::overload_cast<const std::optional< ::smoke::Nullable::SomeEnum >&>(&Nullable::set_enum_property))
        .def_property("array_property", py::overload_cast<>(&Nullable::get_array_property, py::const_), py::overload_cast<const std::optional< ::std::vector< ::std::string > >&>(&Nullable::set_array_property))
        .def_property("inline_array_property", py::overload_cast<>(&Nullable::get_inline_array_property, py::const_), py::overload_cast<const std::optional< ::std::vector< ::std::string > >&>(&Nullable::set_inline_array_property))
        .def_property("map_property", py::overload_cast<>(&Nullable::get_map_property, py::const_), py::overload_cast<const std::optional< ::std::unordered_map< int64_t, ::std::string > >&>(&Nullable::set_map_property))
        .def_property("instance_property", py::overload_cast<>(&Nullable::get_instance_property, py::const_), py::overload_cast<const ::std::shared_ptr< ::smoke::SomeInterface >&>(&Nullable::set_instance_property))
        ;

auto cls_NullableSomeStruct = py::class_<SomeStruct>(cls_Nullable, "SomeStruct")
        .def_readwrite("string_field", &SomeStruct::string_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("string_field"))
        ;

auto cls_NullableNullableStruct = py::class_<NullableStruct>(cls_Nullable, "NullableStruct")
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
        .def(py::init<std::optional< ::std::string >, std::optional< bool >, std::optional< double >, std::optional< ::smoke::Nullable::SomeStruct >, std::optional< ::smoke::Nullable::SomeEnum >, std::optional< ::std::vector< ::std::string > >, std::optional< ::std::vector< ::std::string > >, std::optional< ::std::unordered_map< int64_t, ::std::string > >, ::std::shared_ptr< ::smoke::SomeInterface >>(), py::arg("string_field"), py::arg("bool_field"), py::arg("double_field"), py::arg("struct_field"), py::arg("enum_field"), py::arg("array_field"), py::arg("inline_array_field"), py::arg("map_field"), py::arg("instance_field"))
        ;

auto cls_NullableNullableIntsStruct = py::class_<NullableIntsStruct>(cls_Nullable, "NullableIntsStruct")
        .def_readwrite("int8_field", &NullableIntsStruct::int8_field)
        .def_readwrite("int16_field", &NullableIntsStruct::int16_field)
        .def_readwrite("int32_field", &NullableIntsStruct::int32_field)
        .def_readwrite("int64_field", &NullableIntsStruct::int64_field)
        .def_readwrite("uint8_field", &NullableIntsStruct::uint8_field)
        .def_readwrite("uint16_field", &NullableIntsStruct::uint16_field)
        .def_readwrite("uint32_field", &NullableIntsStruct::uint32_field)
        .def_readwrite("uint64_field", &NullableIntsStruct::uint64_field)
        .def(py::init<>())
        .def(py::init<std::optional< int8_t >, std::optional< int16_t >, std::optional< int32_t >, std::optional< int64_t >, std::optional< uint8_t >, std::optional< uint16_t >, std::optional< uint32_t >, std::optional< uint64_t >>(), py::arg("int8_field"), py::arg("int16_field"), py::arg("int32_field"), py::arg("int64_field"), py::arg("uint8_field"), py::arg("uint16_field"), py::arg("uint32_field"), py::arg("uint64_field"))
        ;

auto cls_NullableSomeEnum = py::enum_<SomeEnum>(cls_Nullable, "SomeEnum")
        .value("ON", SomeEnum::ON)
        .value("OFF", SomeEnum::OFF)
        ;


}
