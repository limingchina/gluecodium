

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

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Nullable = ::smoke::Nullable;


void register_smoke_Nullable(py::module_& module) {
    py::class_<Nullable, std::shared_ptr<Nullable>>(module, "smoke_Nullable")
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
}

