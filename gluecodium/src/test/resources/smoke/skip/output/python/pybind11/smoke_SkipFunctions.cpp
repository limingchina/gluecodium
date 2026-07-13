

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SkipFunctions.h"
#include "string"

void register_SkipFunctions(py::module_& module) {
    py::class_<SkipFunctions>(module, "SkipFunctions")
        .def("not_in_java", &SkipFunctions::not_in_java, py::arg("input"))
        .def("not_in_swift", &SkipFunctions::not_in_swift, py::arg("input"))
        .def("not_in_dart", &SkipFunctions::not_in_dart, py::arg("input"))
        .def("not_in_kotlin", &SkipFunctions::not_in_kotlin, py::arg("input"))
        ;
}

