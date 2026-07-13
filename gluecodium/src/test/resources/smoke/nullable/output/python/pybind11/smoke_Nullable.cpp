

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/VectorHash.h"
#include "smoke/Nullable.h"
#include "smoke/SomeInterface.h"
#include "cstdint"
#include "memory"
#include "optional"
#include "string"
#include "vector"

void register_Nullable(py::module_& module) {
    py::class_<Nullable>(module, "Nullable")
        .def("method_with_string", &Nullable::method_with_string, py::arg("input"))
        .def("method_with_boolean", &Nullable::method_with_boolean, py::arg("input"))
        .def("method_with_double", &Nullable::method_with_double, py::arg("input"))
        .def("method_with_int", &Nullable::method_with_int, py::arg("input"))
        .def("method_with_some_struct", &Nullable::method_with_some_struct, py::arg("input"))
        .def("method_with_some_enum", &Nullable::method_with_some_enum, py::arg("input"))
        .def("method_with_some_array", &Nullable::method_with_some_array, py::arg("input"))
        .def("method_with_inline_array", &Nullable::method_with_inline_array, py::arg("input"))
        .def("method_with_some_map", &Nullable::method_with_some_map, py::arg("input"))
        .def("method_with_instance", &Nullable::method_with_instance, py::arg("input"))
        .def_property("string_property", &Nullable::get_string_property)
        .def_property("is_bool_property", &Nullable::is_bool_property)
        .def_property("double_property", &Nullable::get_double_property)
        .def_property("int_property", &Nullable::get_int_property)
        .def_property("struct_property", &Nullable::get_struct_property)
        .def_property("enum_property", &Nullable::get_enum_property)
        .def_property("array_property", &Nullable::get_array_property)
        .def_property("inline_array_property", &Nullable::get_inline_array_property)
        .def_property("map_property", &Nullable::get_map_property)
        .def_property("instance_property", &Nullable::get_instance_property)
        ;
}

