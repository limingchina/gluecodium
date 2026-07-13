

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/MethodOverloads.h"
#include "cstdint"
#include "string"

void register_MethodOverloads(py::module_& module) {
    py::class_<MethodOverloads>(module, "MethodOverloads")
        .def("is_boolean", &MethodOverloads::is_boolean, py::arg("input"))
        .def("is_boolean", &MethodOverloads::is_boolean, py::arg("input"))
        .def("is_boolean", &MethodOverloads::is_boolean, py::arg("input"))
        .def("is_boolean", &MethodOverloads::is_boolean, py::arg("input"))
        .def("is_boolean", &MethodOverloads::is_boolean, py::arg("input1"), py::arg("input2"), py::arg("input3"), py::arg("input4"))
        .def("is_boolean", &MethodOverloads::is_boolean, py::arg("input"))
        .def("is_boolean", &MethodOverloads::is_boolean, py::arg("input"))
        .def("is_boolean", &MethodOverloads::is_boolean)
        .def("is_float", &MethodOverloads::is_float, py::arg("input"))
        .def("is_float", &MethodOverloads::is_float, py::arg("input"))
        ;
}

