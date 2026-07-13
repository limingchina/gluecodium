

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/off/NestedPackages.h"
#include "string"

void register_NestedPackages(py::module_& module) {
    py::class_<NestedPackages>(module, "NestedPackages")
        .def("basic_method", &NestedPackages::basic_method, py::arg("input"))
        ;
}

