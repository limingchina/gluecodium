

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/Enums.h"
#include "string"

void register_Enums(py::module_& module) {
    py::class_<Enums>(module, "Enums")
        .def("method_with_enumeration", &Enums::method_with_enumeration, py::arg("input"))
        .def("flip_enum_value", &Enums::flip_enum_value, py::arg("input"))
        .def("extract_enum_from_struct", &Enums::extract_enum_from_struct, py::arg("input"))
        .def("create_struct_with_enum_inside", &Enums::create_struct_with_enum_inside, py::arg("type"), py::arg("message"))
        ;
}

