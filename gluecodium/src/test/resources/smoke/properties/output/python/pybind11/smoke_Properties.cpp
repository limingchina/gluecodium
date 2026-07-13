

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/VectorHash.h"
#include "smoke/Properties.h"
#include "smoke/PropertiesInterface.h"
#include "cstdint"
#include "memory"
#include "string"
#include "vector"

void register_Properties(py::module_& module) {
    py::class_<Properties>(module, "Properties")
        .def_property("built_in_type_property", &Properties::get_built_in_type_property)
        .def_property("readonly_property", &Properties::get_readonly_property)
        .def_property("struct_property", &Properties::get_struct_property)
        .def_property("array_property", &Properties::get_array_property)
        .def_property("complex_type_property", &Properties::get_complex_type_property)
        .def_property("byte_buffer_property", &Properties::get_byte_buffer_property)
        .def_property("instance_property", &Properties::get_instance_property)
        .def_property("is_boolean_property", &Properties::is_boolean_property)
        .def_property("static_property", &Properties::get_static_property)
        .def_property("static_readonly_property", &Properties::get_static_readonly_property)
        ;
}

