

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SkipPlatforms.h"
#include "string"

void register_SkipPlatforms(py::module_& module) {
    py::class_<SkipPlatforms>(module, "SkipPlatforms")
        .def("not_in_java", &SkipPlatforms::not_in_java, py::arg("input"))
        .def("not_in_swift", &SkipPlatforms::not_in_swift, py::arg("input"))
        .def("not_in_dart", &SkipPlatforms::not_in_dart, py::arg("input"))
        .def("not_in_kotlin", &SkipPlatforms::not_in_kotlin, py::arg("input"))
        ;
}

