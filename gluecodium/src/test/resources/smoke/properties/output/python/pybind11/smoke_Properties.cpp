

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/VectorHash.h"
#include "smoke/Properties.h"
#include "smoke/PropertiesInterface.h"
#include "cstdint"
#include "memory"
#include "string"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Properties = ::smoke::Properties;

void register_Properties(py::module_& module) {
    py::class_<Properties, std::shared_ptr<Properties>>(module, "Properties")
        .def_property("built_in_type_property", py::overload_cast<>(&Properties::get_built_in_type_property, py::const_), py::overload_cast<const uint32_t>(&Properties::set_built_in_type_property))
        .def_property_readonly("readonly_property", py::overload_cast<>(&Properties::get_readonly_property, py::const_))
        .def_property("struct_property", py::overload_cast<>(&Properties::get_struct_property, py::const_), py::overload_cast<const ::smoke::Properties::ExampleStruct&>(&Properties::set_struct_property))
        .def_property("array_property", py::overload_cast<>(&Properties::get_array_property, py::const_), py::overload_cast<const ::std::vector< ::std::string >&>(&Properties::set_array_property))
        .def_property("complex_type_property", py::overload_cast<>(&Properties::get_complex_type_property, py::const_), py::overload_cast<const ::smoke::Properties::InternalErrorCode>(&Properties::set_complex_type_property))
        .def_property("byte_buffer_property", py::overload_cast<>(&Properties::get_byte_buffer_property, py::const_), py::overload_cast<const ::std::shared_ptr< ::std::vector< uint8_t > >&>(&Properties::set_byte_buffer_property))
        .def_property("instance_property", py::overload_cast<>(&Properties::get_instance_property, py::const_), py::overload_cast<const ::std::shared_ptr< ::smoke::PropertiesInterface >&>(&Properties::set_instance_property))
        .def_property("is_boolean_property", py::overload_cast<>(&Properties::is_boolean_property, py::const_), py::overload_cast<const bool>(&Properties::set_boolean_property))
        .def_property("static_property", py::overload_cast<>(&Properties::get_static_property, py::const_), py::overload_cast<const ::std::string&>(&Properties::set_static_property))
        .def_property_readonly("static_readonly_property", py::overload_cast<>(&Properties::get_static_readonly_property, py::const_))
        ;
}

